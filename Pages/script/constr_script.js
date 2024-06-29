let chg_button = document.querySelector(".submit-button");
let inputs = document.querySelectorAll("input[type=text], input[type=tel], input[type=email]");
let secondPhone = document.querySelector(".phone2");
let example_fields = [];
let labels = [];
for (let i = 0; i < inputs.length; i++) {
	labels.push(inputs[i].previousElementSibling);
}
example_fields = document.getElementsByClassName("card-item");

function findCardItem(item_name) {
	for (let i = 0; i < example_fields.length; i++) {
		if (example_fields[i].classList.contains(item_name)) {
			return example_fields[i];
		}
	}
}

let checkRequires = function () {
	for (let i = 0; i < inputs.length; i++) {
		if (labels[i]) {
			if (inputs[i].required) {
				if (labels[i].innerHTML.indexOf("*") === -1) labels[i].innerHTML += " *";
			}
			else {
				labels[i].innerHTML = labels[i].innerHTML.replace(/\*/g, "");
			}
		}
	}
}
checkRequires();

let radioButtons = document.querySelectorAll("input[type=radio]");
for (let i = 0; i < radioButtons.length; i++) {
	radioButtons[i].addEventListener('click', paintPalette);	
}
function paintPalette () {
	for (let i = 0; i < radioButtons.length; i++) {
	if (radioButtons[i].name === "color" || radioButtons[i].name === "color2") {
		if (radioButtons[i].checked) {
			radioButtons[i].parentElement.classList.remove("not-checked");
			radioButtons[i].parentElement.classList.add("checked");
		} else {
			radioButtons[i].parentElement.classList.remove("checked");
			radioButtons[i].parentElement.classList.add("not-checked");
		}
	}
}
}
paintPalette();

let name_field = findCardItem("name-card-example");
let position_field = findCardItem("position-card-example");
let setPreferences = function(object) {
		switch (object.name) {
			case "straigthen":
				name_field.style.textAlign = object.value;
				break;
			case "straigthen2":
				position_field.style.textAlign = object.value;
				break;
			case "fsize":
				name_field.style.fontSize = object.value;
				break;
			case "fsize2":
				position_field.style.fontSize = object.value;
				break;
			case "color":
				name_field.style.color = object.value;
				break
			case "color2":
				position_field.style.color = object.value;
				break;
			default:
				break;
		}
	}

let addPhone = document.querySelector(".addPhone");
let removePhone = document.querySelector(".removePhone");
let innerBlock = document.querySelector(".inner-block");
let hiddenBlock = document.querySelector(".hidden-block");

// let secondPhoneField = findCardItem("phone2-card-example");
// addPhone.addEventListener('click', function() {
// 	secondPhone.value = "";
// 	secondPhoneField.innerHTML = "";
// 	hiddenBlock.classList.toggle("none");
// 	innerBlock.classList.toggle("none");
// 	secondPhoneField.classList.remove("none");
// 	secondPhone.setAttribute("required", "required");
// });
// removePhone.addEventListener('click', function() {
// 	hiddenBlock.classList.toggle("none");
// 	innerBlock.classList.toggle("none");
// 	secondPhoneField.classList.add("none");
// 	secondPhone.value = "no_extra_phone";
// 	secondPhone.removeAttribute("required");
// });

let showMail = document.querySelector(".showMail");
let showLocation = document.querySelector(".showLocation");
showMail.addEventListener('click', function () {
	if (!showMail.checked) { 
		mail_input.removeAttribute("required");
	} else {
		mail_input.setAttribute("required", "required");
	}
	checkRequires();
});
showLocation.addEventListener('click', function () {
	if (!showLocation.checked) {
		location_input.removeAttribute("required");
	} else {
		location_input.setAttribute("required", "required");
	}
	checkRequires();
});

let mail_field = findCardItem("mail-card-example");
let location_field = findCardItem("location-card-example");
let mail_input = document.querySelector(".mail");
let location_input = document.querySelector(".location");
let showData = function (object) {
	if (object.classList.contains("showMail")) {
		if (!object.checked) {
			mail_field.classList.add("none");
		} else {
			mail_field.classList.remove("none");
		}	
	} else if (object.classList.contains("showLocation")) {
		if (!object.checked) {
			location_field.classList.add("none");
		} else {
			location_field.classList.remove("none");
		}
	}
}

chg_button.addEventListener('click', function() {
	empty = false;
	showData(showMail);
	showData(showLocation);
	for (let i = 0; i < inputs.length; i++) {
		if (inputs[i].value === "" && inputs[i].required) {
			empty = true;
			inputs[i].style.borderColor = "#d5265b";
		}
		else {
			inputs[i].style.borderColor = "rgb(156,156,156)";
		}
	}
	if (empty) {
		alert("Пожалуйста, заполните все поля!");
		return;
	}
	for (let i = 0; i < inputs.length; i++) {
		example_fields[i].innerHTML = inputs[i].value; 
	}
	for (let i = 0; i < radioButtons.length; i++) {
		if (radioButtons[i].checked === true) {
			setPreferences(radioButtons[i]);
		}
	}
});


function readURL(input) {
	if (input.files && input.files[0]) {
		var reader = new FileReader();
		reader.onload = function(e) {
		$('.image-upload-wrap').hide();
		$('.file-upload-image').attr('src', e.target.result);
		$('.file-upload-content').show();
		$('.image-title').html(input.files[0].name);
		};
		reader.readAsDataURL(input.files[0]);
	} else {
		removeUpload();
	}
	}
	function removeUpload() {
	$('.file-upload-input').replaceWith($('.file-upload-input').clone());
	$('.file-upload-content').hide();
	$('.image-upload-wrap').show();
	}
	$('.image-upload-wrap').bind('dragover', function () {
			$('.image-upload-wrap').addClass('image-dropping');
		});
		$('.image-upload-wrap').bind('dragleave', function () {
			$('.image-upload-wrap').removeClass('image-dropping');
});

function readURL2(input2) {
	if (input2.files && input2.files[0]) {
		var reader = new FileReader();
		reader.onload = function(e) {
		$('.image-upload-wrap2').hide();
		$('.file-upload-image2').attr('src', e.target.result);
		$('.file-upload-content2').show();
		$('.image-title2').html(input2.files[0].name);
		};
		reader.readAsDataURL(input2.files[0]);
	} else {
		removeUpload2();
	}
	}
	function removeUpload2() {
	$('.file-upload-input2').replaceWith($('.file-upload-input2').clone());
	$('.file-upload-content2').hide();
	$('.image-upload-wrap2').show();
	}
	$('.image-upload-wrap2').bind('dragover', function () {
			$('.image-upload-wrap2').addClass('image-dropping2');
		});
		$('.image-upload-wrap2').bind('dragleave', function () {
			$('.image-upload-wrap2').removeClass('image-dropping2');
});
