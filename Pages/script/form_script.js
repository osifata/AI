const previousButton = document.querySelector('#prev')
const nextButton = document.querySelector('#next')
const submitButton = document.querySelector('#submit')
const tabTargets = document.querySelectorAll('.tab')
const tabPanels = document.querySelectorAll('.tabpanel')
const isEmpty = (str) => !str.trim().length
let currentStep = 0


validateEntry()

nextButton.addEventListener('click', (event) => {
  event.preventDefault()

  tabPanels[currentStep].classList.add('hidden')
  tabTargets[currentStep].classList.remove('active')

  tabPanels[currentStep + 1].classList.remove('hidden')
  tabTargets[currentStep + 1].classList.add('active')
  currentStep += 1
  
  validateEntry()
  updateStatusDisplay()
})

previousButton.addEventListener('click', (event) => {
  event.preventDefault()

  tabPanels[currentStep].classList.add('hidden')
  tabTargets[currentStep].classList.remove('active')

  tabPanels[currentStep - 1].classList.remove('hidden')
  tabTargets[currentStep - 1].classList.add('active')
  currentStep -= 1

  nextButton.removeAttribute('disabled')
  updateStatusDisplay()
})


function updateStatusDisplay() {
  if (currentStep === tabTargets.length - 1) {
    nextButton.classList.add('hidden')
    previousButton.classList.remove('hidden')
    submitButton.classList.remove('hidden')
    validateEntry()

  } else if (currentStep == 0) {
    nextButton.classList.remove('hidden')
    previousButton.classList.add('hidden')
    submitButton.classList.add('hidden')
  } else {
    nextButton.classList.remove('hidden')
    previousButton.classList.remove('hidden')
    submitButton.classList.add('hidden')
  }
}

function validateEntry() {
  let input = tabPanels[currentStep].querySelector('.form-input')
  let input2 = tabPanels[currentStep].querySelector('.form-input2')
  let inputAll = tabPanels[currentStep].querySelectorAll('.form-input2')
  let select = tabPanels[currentStep].querySelector('.select-input')
  let checkboxes = tabPanels[currentStep].querySelectorAll('input[type="checkbox"]')

  function atLeastOneCheckboxChecked(checkboxes) {
    return Array.from(checkboxes).some(checkbox => checkbox.checked);
  }

  nextButton.setAttribute('disabled', true)
  submitButton.setAttribute('disabled', true)

  if (input && input2) {
    inputAll.forEach(element => {
      setButtonPermissions(element); 
      element.addEventListener('input', () => setButtonPermissions(element))
    });
  } else if (input || select || checkboxes) {
      if (input) {
        setButtonPermissions(input)
        input.addEventListener('input', () => setButtonPermissions(input))
      }
      if (select) {
        select.addEventListener('change', function() {
          if (this.value == '0') {
            nextButton.setAttribute('disabled', true)
            submitButton.setAttribute('disabled', true)
          } else{
            nextButton.removeAttribute('disabled')
            submitButton.removeAttribute('disabled')
          }
        });
      }
      if (checkboxes) {
        checkboxes.forEach(function(checkbox) {
          checkbox.addEventListener('change', function() {
            if (!atLeastOneCheckboxChecked(checkboxes)) {
              nextButton.setAttribute('disabled', true)
              submitButton.setAttribute('disabled', true)
            } else { 
              nextButton.removeAttribute('disabled')
              submitButton.removeAttribute('disabled')
            }
          })
        });
      }
  }
}

function setButtonPermissions(input) {
  if (isEmpty(input.value)) {
    nextButton.setAttribute('disabled', true)
    submitButton.setAttribute('disabled', true)
  } else {
    nextButton.removeAttribute('disabled')
    submitButton.removeAttribute('disabled')
  }
}
