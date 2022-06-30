

const csv = require('csv-parser');
const fs = require('fs');
const errorLog = require('fs');
const HashTable = require('./HashTable');
const datafile = require('fs');
const puppeteer = require('puppeteer-extra');
const randomUseragent = require('random-useragent');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');

puppeteer.use(StealthPlugin())

const chromeOptions = {
    headless:false,
    defaultViewport: null,
    slowMo:10,
  };

(async function main() {

  //Create the Hashtable object to store the property information 
  const theHashTable = new HashTable();  
  
  var data = require("fs").readFileSync("All_Parcels_NE&NW.csv", "utf8");
  data = data.split("\r\n")
  for (let i of data) { data[i] = data[i]}

  datafile.open('theData.txt', 'w', function(err, f){
    
  })

  datafile.open('Errors.txt', 'w', function(err, f){
    
})


  parcelNum = data[1];

  //Split the parcel number so that each segment can be input into the form
  splitParcel = parcelNum.split('-');
 
  const browser = await puppeteer.launch(chromeOptions);
  const page = await browser.newPage();

  await page.goto('https://www.accesskent.com/Property/');

  //Enter the parcel number and wait for the user to complete the ReCaptcha
  await page.type('#parcelNo2', splitParcel[1]);
  await page.type('#parcelNo3', splitParcel[2]);
  await page.type('#parcelNo4', splitParcel[3]);
  await page.type('#parcelNo5', splitParcel[4]);

  await page.waitFor(20000);

  //Click the Search button after completing ReCaptcha
  await page.click('#PropSearch2 > div > fieldset > div:nth-child(4) > div > input');
  await page.waitForSelector('body > div.off-canvas-wrapper > div > div.row.apps.main-content > div > form > table > tbody > tr > td:nth-child(2) > a');
  await page.click('body > div.off-canvas-wrapper > div > div.row.apps.main-content > div > form > table > tbody > tr > td:nth-child(2) > a');
  
  //This number will be used to append the data to a text file every 20 parcel numbers
  const modNumber = 20;

  for(let x = 1802; x < data.length; x++){

      parcelNum = data[x]
    
      //Get the property info from the first page afer stepping into the parcel number link
      await page.waitForSelector('body > div.off-canvas-wrapper > div > div.row.apps.main-content > div > form > fieldset > div > div:nth-child(1) > p');
      var propertyInfo = await getPropertyInfo(page);
    
      
      //step into the delinquent tab to get tax money owed
      await page.waitForSelector('#parcel-nav > ul > li:nth-child(6) > a');
      await page.click('#parcel-nav > ul > li:nth-child(6) > a');
    
      var delinquentInfo = await getDelinquentInfo(page, parcelNum);

      //step into the Sales History tab to get Sales history & additional property info
      await page.waitForSelector('#parcel-nav > ul > li:nth-child(2) > a')
      await page.click('#parcel-nav > ul > li:nth-child(2) > a')

      var salesHistory = await getSalesHistory(page);
      

      //Combine the data from the delinquent tab with the property info
      var allData = propertyInfo
      allData.push(delinquentInfo + '>>\n')
      allData.push(salesHistory + '>>\n')
      console.log(allData);
      
      parcelNum2 = parseInt(parcelNum.replace(/-/g, ""))

      theHashTable.set(parcelNum2, allData)

      //Every 20 parcel numbers, write the data to the textfile
      if((x % modNumber) == 0){

          writeData(theHashTable);

      }
    
      //Go to the next property by modifying the URL by inputting the next parcel number. This avoids having to complete another ReCaptcha
      await page.goto('https://www.accesskent.com/Property/realEstate.do?parcelNo='+parcelNum+'&ele=1');
    
  }

})()

async function getPropertyInfo(page){

    var propInfo = await page.evaluate(()=>{
        var textblock = Array.from(document.querySelectorAll('body > div.off-canvas-wrapper > div > div.row.apps.main-content > div > form > fieldset > div > div:nth-child(1) > p'));
        return textblock.map(p => p.innerText.replace(/^\s+|\s+$/g, '').trim());
    })  

    return propInfo;
}

async function getDelinquentInfo(page, parcelNum){
    try{
        await page.waitForSelector('body > div.off-canvas-wrapper > div > div.row.apps.main-content > div > form > fieldset > table > tbody > tr > td:nth-child(2)');
        var data = await page.evaluate(()=>{
            var tds = Array.from(document.querySelectorAll('td:nth-child(3)'));
            return tds.map(td => td.innerText.replace(/^\s+|\s+$/g, '').trim());
        });
    }catch{

        errorLog.appendFile('Errors.txt', parcelNum, (err) => {
            if(err) throw err;
        })

        var data = '$0.00'
    }

    return data;
}

async function getSalesHistory(page){
try{
    await page.waitForSelector('body > div.off-canvas-wrapper > div > div.row.apps.main-content > div > form > fieldset > table > tbody > tr:nth-child(1)') 
    var propInfo = await page.evaluate(()=>{
        var textblock = Array.from(document.querySelectorAll('body > div.off-canvas-wrapper > div > div.row.apps.main-content > div > form > fieldset > table > tbody > tr:nth-child(1)'));
        return textblock.map(p => p.innerText.replace(/^\s+|\s+$/g, '').trim());
    });
}catch{
    errorLog.appendFile('Errors.txt', parcelNum, (err) => {
        if(err) throw err;
    })

    var data = ',>>\n'
}  

    return propInfo;
}



function writeData(theHashTable){
    dataCounter = 0
    for(let j = 0; j < theHashTable.size; j++){
        if(typeof theHashTable.buckets[j] != 'undefined'){
            nodeData = theHashTable.buckets[j].tail
            datafile.appendFile('theData.txt',  nodeData.data.toString(), (err) => {
                if(err) throw err;
            })
            dataCounter += 1
           
            nodeData = nodeData.next
            while(nodeData != null){
                datafile.appendFile('theData.txt', nodeData.data.toString(), (err) => {
                    if(err) throw err;
                    dataCounter += 1
                })
                
                nodeData = nodeData.next
            }
        }
    }
}



