let jsVariable = JSON.parse(document.getElementById('homework-words').textContent);


const App = {
    data() {
        return {
            jsVariable,
            dobleJsVariable: {},
            jsVariableValue: {},
            engWord: '',
            rusWord: '',
            allVal: [],
            message: 'Выберите ответ',
            messageFirst: 'Учим слова',
            activeClass: 'alert-info',
            dispStart: 'd-none',
            btnStart: 'd-inline',
            imgStart: 'd-none',
            listTest: {},
            countWord: {},
            btnNext: 'd-none',
            secondStage: 'd-inline',
            activeDisplay: 'inline',
            activeDisplaySecond: 'none',
            inputValue: '',
            gif: 'none',            
        }
    },
    methods: {
        showDict(val){
            const randomKey = Object.keys(val)
            let a = randomKey[Math.floor(Math.random()*randomKey.length)]
            this.engWord = a
            this.rusWord = val[a]
        },
        allValue(val) {
            let arrWord = []
            let sliceWord = []
            for(item in val) {
                arrWord.push(val[item])
            }
            count = 0
            for(item in arrWord) {
                if (arrWord.length >=5){
                    b = Math.floor(Math.random() * arrWord.length)
                    sliceWord.push(arrWord[b]);
                    arrWord.splice(b, 1);
                } 
            }
            if(arrWord.indexOf(this.rusWord) === -1) {
                arrWord.push(this.rusWord)
            } else {
                arrWord.push(sliceWord[0]);
            }
            this.allVal = arrWord
        },
        forList() {
            for (i in jsVariable) {
                this.countWord[i] = 0;
            }
        },

        inputClick(event) {
            if (Object.keys(this.countWord).length == 0) {
                this.forList()
            }
            if (Object.keys(this.dobleJsVariable).length == 0) {
                for (i in jsVariable) {
                    this.dobleJsVariable[i] = jsVariable[i];
                }
            }

            if (event.target.value == this.rusWord){
                this.countWord[this.engWord] ++
                if (this.countWord[this.engWord] > 3) {
                    delete this.dobleJsVariable[this.engWord]
                }
                if (Object.keys(this.dobleJsVariable).length == 0) {
                    this.btnNext = 'd-inline'
                    
                }
                this.activeClass = 'alert-success'
                this.message = "Вы ответили верно"
                this.showDict(this.dobleJsVariable);
                this.allValue(this.jsVariableValue);
            }
            else {
                this.countWord[this.engWord] -- 
                this.activeClass = 'alert-danger'
                this.message = "Ваш ответ не верен"  
            }
        },
        addValAll() {
            for (i in jsVariable) {
                this.jsVariableValue[i] = jsVariable[i]
            }
        },
        inputStart() {
            this.btnStart = 'd-none'
            this.imgStart = 'd-inline'
            this.dispStart = 'd-block'
            this.showDict(jsVariable);
            this.allValue(jsVariable);
            this.addValAll()
        },

        // Второй этап проверки слов
        showDictSecond(val){
            const randomKey = Object.keys(val)
            let a = randomKey[Math.floor(Math.random()*randomKey.length)]
            this.engWord = a
            this.rusWord = val[a]

        },

        secondStageGo() {
            this.activeDisplay = 'none'
            this.activeDisplaySecond = 'inline'
            this.message = 'Введите ответ'
            this.activeClass = 'alert-info'
            this.countWord = {}
            this.showDictSecond(jsVariable)
        },
        clickValid() {
            if (Object.keys(this.countWord).length == 0) {
                for (i in jsVariable) {
                    this.countWord[jsVariable[i]] = 0;
                }
            }
            if(this.inputValue == this.engWord) {
                this.countWord[this.rusWord] ++
                if (this.countWord[this.rusWord] > 3) {
                    delete this.jsVariable[this.engWord]
                }
                if (Object.keys(this.jsVariable).length == 0) {
                    this.activeDisplaySecond = 'none'
                    this.messageFirst = 'Поздравляю!'
                    this.gif = 'inline'
                }
                this.activeClass = 'alert-success'
                this.message = "Вы ответили верно"
                this.showDictSecond(this.jsVariable);
                this.allValue(this.jsVariableValue);
                this.inputValue = ''

            }
            else {
                this.countWord[this.rusWord] -- 
                this.activeClass = 'alert-danger'
                this.message = "Ваш ответ не верен"
                this.inputValue = ''
            }
        },        
        validNext(event) {
            if(event.key === 'Enter') {
                this.clickValid()
            }
        },
        inputControl(event) {
            this.inputValue = (event.target.value).trim()
        }

    },


}


Vue.createApp(App).mount('#study_app_one')
