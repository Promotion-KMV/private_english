document.addEventListener('DOMContentLoaded', () => { 
    const showAccordion = document.querySelectorAll('.collapse')
    const btn = document.querySelectorAll('button')
    btn.forEach((item) => {
        item.addEventListener('click', (e) => {
            if (item.attributes[1].value == 'true') {
                btn.forEach((item) => {
                    item.setAttribute('disabled', 'disabled');
                })
            item.removeAttribute('disabled', 'disabled')
            } else {
                btn.forEach((item) => {
                    item.removeAttribute('disabled', 'disabled')
                
                })
            }
        })
    })
})