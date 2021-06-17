let jsVariable = JSON.parse(document.getElementById('study_words').textContent);
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
            btnNextTwo: 'd-none',
            secondStage: 'd-inline',
            activeDisplay: 'inline',
            activeDisplaySecond: 'none',
            activeDisplayThree: 'none',
            inputValue: '',
            gif: 'none',
            NumberAttempts: 3,
            ActiveCount: 0,
            countP: 1,
            countWordProgress: 0,
            
        }
    },
    methods: {
        CountProgress() {
        // Метод для  Прогрессбара(высчитываем 100%)
            let count = 0;
            for (let key in jsVariable) {
                count++
            }
            this.countWordProgress = count * (this.NumberAttempts + 1)
        },

        UpdateActiveCount(count) {
            // Изменения Процентов в прогресбаре
            this.ActiveCount = Math.round(((count - 1) * 100) / this.countWordProgress)
        },

        showDict(val){
            // Вывод случайного слова
            const randomKey = Object.keys(val)
            let a = randomKey[Math.floor(Math.random()*randomKey.length)]
            this.engWord = a
            this.rusWord = val[a]
        },

        allValue(val) {
            //функция для вывода слов на русском языке
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
        allValueTwo(val) {
            //функция для вывода слов на английском языке
            let arrWord = []
            let sliceWord = []
            for(item in val) {
                arrWord.push(item)
            }
            count = 0
            for(item in arrWord) {
                if (arrWord.length >=5){
                    b = Math.floor(Math.random() * arrWord.length)
                    sliceWord.push(arrWord[b]);
                    arrWord.splice(b, 1);
                } 
            }
            if(arrWord.indexOf(this.engWord) === -1) {
                arrWord.push(this.engWord)
            } else {
                arrWord.push(sliceWord[0]);
            }
            this.allVal = arrWord
        },
        forList(count, item) {
            //Добавляем записи в счетчик
            for (i in item) {
                count[i] = 0;
            }
        },

        inputClick(event) {
            // выбор слов на русском языке(по клику)
            if (Object.keys(this.countWord).length == 0) {
                this.forList(this.countWord, jsVariable)
            }
            if (Object.keys(this.dobleJsVariable).length == 0) {
                for (i in jsVariable) {
                    this.dobleJsVariable[i] = jsVariable[i];
                }
            }

            if (event.target.value == this.rusWord){
                this.countP ++
                this.UpdateActiveCount(this.countP)
                this.countWord[this.engWord] ++
                if (this.countWord[this.engWord] > this.NumberAttempts) {
                    delete this.dobleJsVariable[this.engWord]
                }
                if (Object.keys(this.dobleJsVariable).length == 0) {
                    this.btnNextTwo = 'd-inline'
                    this.ActiveCount = 0
                    this.countP = 1
                }
                this.activeClass = 'alert-success'
                this.message = "Вы ответили верно"
                this.showDict(this.dobleJsVariable);
                this.allValue(this.jsVariableValue);

            }
            else {
                this.countP --
                this.UpdateActiveCount(this.countP)
                this.countWord[this.engWord] -- 
                this.activeClass = 'alert-danger'
                this.message = "Ваш ответ не верен"  
            }
        },
        addValAll() {
            // Добавляем значения для резервного хранения слов
            for (i in jsVariable) {
                this.jsVariableValue[i] = jsVariable[i]
            }
        },
        inputStart() {
            // По нажатию открывается первое поля для изучения
            this.btnStart = 'd-none'
            this.imgStart = 'd-inline'
            this.dispStart = 'd-block'
            this.showDict(jsVariable);
            this.allValue(jsVariable);
            this.addValAll()
        },

        ThreeStageGo() {
            // По нажатию открывается второй блок изучения слов
            this.activeDisplay = 'none'
            this.activeDisplaySecond = 'inline'
            this.btnNextTwo = 'd-none'
            this.message = 'Введите ответ'
            this.activeClass = 'alert-info'
            this.countWord = {}
            this.showDict(this.jsVariableValue)
            this.allValueTwo(this.jsVariableValue);
        },
        clickValid() {
            // функция изучения слов путем ввода правильного ответа
            if (Object.keys(this.countWord).length == 0) {
                for (i in jsVariable) {
                    this.countWord[jsVariable[i]] = 0;
                }
            }
            if(this.inputValue == this.engWord) {
                this.countWord[this.rusWord] ++
                this.countP ++
                this.UpdateActiveCount(this.countP)
                if (this.countWord[this.rusWord] > this.NumberAttempts) {
                    delete this.jsVariable[this.engWord]
                }
                if (Object.keys(this.jsVariable).length == 0) {
                    this.activeDisplayThree = 'none'
                    this.countWord = {}
                    this.ActiveCount = 0
                    this.countP = 1
                    this.messageFirst = 'Поздравляю!'
                    this.gif = 'inline'
                }
                this.activeClass = 'alert-success'
                this.message = "Вы ответили верно"
                this.showDict(this.jsVariable);
                this.allValue(this.jsVariableValue);
                this.inputValue = ''

            }
            else {
                this.countP --
                this.UpdateActiveCount(this.countP)
                this.countWord[this.rusWord] -- 
                this.activeClass = 'alert-danger'
                this.message = "Ваш ответ не верен"
                this.inputValue = ''
            }
        },

        secondStageGo() {
            // По нажатию открывается третий блок изучения слов
            this.activeDisplay = 'none'
            this.activeDisplayThree = 'inline'
            this.activeDisplaySecond = 'none'
            this.btnNext = 'd-none'
            this.showDict(this.jsVariableValue);
            // this.allValueTwo(this.jsVariableValue);
        },

        inputClickTwo(event) {
            // выбор слов на английском языке(по клику)
            console.log(this.dobleJsVariable)
            if (Object.keys(this.listTest).length == 0) {
                this.forList(this.listTest, jsVariable)
            }
            if (Object.keys(this.dobleJsVariable).length == 0) {
                for (i in this.jsVariableValue) {
                    this.dobleJsVariable[i] = this.jsVariableValue[i];
                }
            }

            if (event.target.value == this.engWord){
                this.countP ++
                this.UpdateActiveCount(this.countP)
                this.listTest[this.engWord] ++
                if (this.listTest[this.engWord] > this.NumberAttempts) {
                    delete this.dobleJsVariable[this.engWord]
                }
                if (Object.keys(this.dobleJsVariable).length == 0) {
                    this.activeDisplayThree = 'none'
                    this.btnNext = 'd-inline'
                    this.ActiveCount = 0
                    this.countP = 1                    
                }

                this.activeClass = 'alert-success'
                this.message = "Вы ответили верно"
                this.showDict(this.dobleJsVariable);
                this.allValueTwo(this.jsVariableValue);

            }
            else {
                this.countP --
                this.UpdateActiveCount(this.countP)
                this.listTest[this.engWord] -- 
                this.activeClass = 'alert-danger'
                this.message = "Ваш ответ не верен"  
            }
        },
        validNext(event) {
            // Проверка правильности ввода слова нажатием н
            if(event.key === 'Enter') {
                this.clickValid()
            }
        },
        inputControl(event) {
            this.inputValue = (event.target.value).trim()
        }

    },
    created() {
        this.CountProgress()
    }
}

Vue.createApp(App).mount('#study_app_words')