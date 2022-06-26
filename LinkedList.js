
class LinkedList{
    constructor(){
        this.head = null
        this.tail = null
        this.size = 0
    }

    addNode(node){

        var current

        if(this.head == null){
            this.head = node
            this.tail = node
        }else{
            current = this.tail

            while(current.next){
                current = current.next
            }

            current.next = node
            this.head = node
        }
        this.size++
    }

    replaceNode(oneNode, position, oneList){

        if(position == oneList.size){
            oneList.head = oneNode
        }else if(position == 0){
            oneNode.next = oneList.tail.next
            oneList.tail.next = null
            oneList.tail = oneNode

        }else{

            var current = oneList.tail
            var prev = null
            for(let i = 0; i < position; i++){
                prev = current
                current = current.next
            }
    
            prev.next = oneNode
            oneNode.next = current.next
            current.next = null

        }

    }
    
}

module.exports = LinkedList