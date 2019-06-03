    class Login {
        constructor() {
            this.login = false;
            this.email = '';
            this.password = '';
            this.data = {};
            this.contentHeader = {};
            this.modalTitle = document.querySelector('.modal-login .modal-title');
            this.button = document.querySelector('.modal-login .modal-footer .login-btn');
            this.URL = `${window.location.origin}/api/v1/`;
            this.API = '';
            this.getIsLogin();
        }

        init() {
            this.getCookiesData();
            this.renderModalLoginForm();
            this.onclickLogin();
            document.querySelector('.modal-login .modal-footer .render_registration_modal').onclick = () => {
                new Register();
            }
        }

        getIsLogin() {
            fetch(`${this.URL}user/`)
            .then(function(response) {
                return response.json();
            })
            .then(data => {
                if (data.detail ===  "Authentication credentials were not provided.") {
                    this.login = false;
                }
                if (data.email) {
                    this.login = true;
                }
                this.init()
            })
            .catch(error => console.log(error));
        }

        renderModalLoginForm() {
            if (this.login) {
                document.querySelector('.modal-login .render_registration_modal').style.display = 'none';
                document.querySelector('.modal-login .request_registration').style.display = 'none';
                document.querySelector('.modal-login .modal-body').style.display = 'none';
                document.querySelector('.modal-login .registration-by-vk').style.display = 'none';
                document.querySelector('.modal-login .registration-by-github').style.display = 'none';

                document.querySelector('#basket-button').style.display = 'block';
                document.querySelector('#like-button').style.display = 'block';
                document.querySelector('#non-logged-in').style.display = 'none';
                document.querySelector('#non-logged-in').style.position = 'absolute';
                document.querySelector('#logged-in').style.display = 'block';
                document.querySelector('#logged-in').style.position = 'static';
                this.button.innerText = 'Выйти';
                this.modalTitle.innerText = 'Выйти из сайта';
            }
            else {
                document.querySelector('.modal-login .render_registration_modal').style.display = 'block';
                document.querySelector('.modal-login .request_registration').style.display = 'none';
                document.querySelector('.modal-login .modal-body').style.display = 'block';
                document.querySelector('.modal-login .password_2').style.display = 'none';
                document.querySelector('.modal-login .first_name').style.display = 'none';
                document.querySelector('.modal-login .date_of_birth').style.display = 'none';
                document.querySelector('.modal-login .registration-by-vk').style.display = 'none';
                document.querySelector('.modal-login .registration-by-github').style.display = 'none';

                document.querySelector('#basket-button').style.display = 'none';
                document.querySelector('#like-button').style.display = 'none';
                document.querySelector('#non-logged-in').style.display = 'block';
                document.querySelector('#non-logged-in').style.position = 'static';
                document.querySelector('#logged-in').style.display = 'none';
                document.querySelector('#logged-in').style.position = 'absolute';
                this.button.innerText = 'Войти';
                this.modalTitle.innerText = 'Войти на сайт';
            }
        }

        onclickLogin() {
            const block = document.querySelector('.modal-login .modal-footer .login-btn');
            block.onclick = () => {
                this.getDataLogin();
                this.requestLogin();
            };
        }

        getDataLogin() {
            if (this.login) {
                this.API = `${this.URL}logout/`;
                this.contentHeader = {"Content-Type": "application/json", "X-CSRFToken": this.csrfToken,};
                this.data = {};
            } else {
                this.API = `${this.URL}login/`;
                this.contentHeader = {"Content-Type": "application/json",};
                this.data = {
                    "email": document.querySelector('#defaultForm-email').value,
                    "password": document.querySelector('#defaultForm-pass-1').value
                    };
            }
        }

        requestLogin() {
            fetch(this.API, {
                    method: 'POST',
                    headers: this.contentHeader,
                    body: JSON.stringify(this.data),
            })
            .then(function(response) {
                return response.json();
            })
            .then(data => {
                if (data.detail === "Successfully logged out.") {
                    document.querySelector('.modal-login .modal-header .close').click();
                    this.login = false;
                    this.init();
                }
                if (data.key) {
                    if (this.blockError){
                        this.blockError.remove();
                    }
                    document.querySelector('.modal-login .modal-header .close').click()
                    this.login = true;
                    this.init();

                }
                else if (data.detail && data.detail === "Successfully logged out.") {
                    document.querySelector('.modal-login .modal-header .close').click();
                    this.login = false;
                    this.init();
                }
                else {
                    if (!this.blockError){
                        this.renderErrorLogin();
                    }
                    this.login = false;
                    this.init();
                }
            })
            .catch(error => console.log(error));
        }

         renderErrorLogin() {
            this.blockError = document.createElement('p');
            this.blockError.style.color = '#f92672';
            this.blockError.style.fontWeight  = 'bold';
            this.blockError.innerText = 'Введены неверные учетные данные!';
            document.querySelector('.modal-body').insertAdjacentElement('afterbegin', this.blockError);
        }

        getCookiesData() {
            if (document.cookie && document.cookie !== '') {
                let cookies = document.cookie.split(';');
                for(let el of cookies) {
                    if(el.split('=')[0].replace(/\s/g, '') === "csrftoken") {
                        this.csrfToken = el.split('=')[1]
                    }
                }
            }
        }
    }



    class Register {
        constructor() {
            this.login = false;
            this.data = {};
            this.contentHeader = {};
            this.csrfToken;
            this.API = '';
            this.modalTitle = document.querySelector('.modal-login .modal-title');
            this.URL = `${window.location.origin}/api/v1/`;
            this.init();
        }

        init() {
            this.getCookiesData();
            this.renderFormRegistration();
            this.validatePasDuplicate();
            this.validateDataBirth();
            document.querySelector('.modal-login .modal-footer .request_registration').onclick = () => {
                    this.getDataRegister();
                    this.requestRegister();
            }
        }

        renderFormRegistration() {
            for (let el of document.querySelectorAll('.md-form')) {
                el.style.marginTop= '3.0rem';
            }
            document.querySelector('.modal-login .modal-body').style.display = 'block';
            document.querySelector('.modal-login .password_2').style.display = 'block';
            document.querySelector('.modal-login .first_name').style.display = 'block';
            document.querySelector('.modal-login .date_of_birth').style.display = 'block';

            document.querySelector('.modal-login .render_registration_modal').style.display = 'none';
            document.querySelector('.modal-login .request_registration').style.display = 'block';

            document.querySelector('.modal-login #loginOkButton').style.display = 'none';
            document.querySelector('.modal-login .registration-by-vk').style.display = 'block';
            document.querySelector('.modal-login .registration-by-github').style.display = 'block';
        }

        validatePasDuplicate() {
            document.querySelector('#defaultForm-pass-2').onchange = () => {
                let passwordDuplicate = document.querySelector('#defaultForm-pass-2');
                let pass1 = document.querySelector('#defaultForm-pass-1').value;
                let pass2 = document.querySelector('#defaultForm-pass-2').value;

                if (pass1 === pass2) {
                    passwordDuplicate.classList.remove('invalid');
                    passwordDuplicate.classList.add('valid');
                }
                else {
                    passwordDuplicate.classList.remove('valid');
                    passwordDuplicate.classList.add('invalid');
                }
            }
        }

        validateDataBirth() {
            let dateBirth = document.querySelector('#defaultForm-date_of_birth');

            dateBirth.onchange = () => {
                if (document.querySelector('#defaultForm-date_of_birth').value) {
                    dateBirth.classList.remove('invalid');
                    dateBirth.classList.add('valid');
                }
                else {
                    dateBirth.classList.remove('valid');
                    dateBirth.classList.add('invalid');
                }
            }
        }

        getDataRegister() {
                this.API = `${this.URL}registration/`;
                this.contentHeader = {"Content-Type": "application/json", "X-CSRFToken": this.csrfToken,};
                this.data = {
                    "email": document.querySelector('#defaultForm-email').value,
                    "password1": document.querySelector('#defaultForm-pass-1').value,
                    "password2": document.querySelector('#defaultForm-pass-2').value,
                    "first_name": document.querySelector('#defaultForm-first_name').value,
                    "date_of_birth": document.querySelector('#defaultForm-date_of_birth').value,
                    };
        }

        requestRegister() {
            console.log('contentHeader', this.contentHeader);
            console.log('data', this.data);
            fetch(this.API, {
                    method: 'POST',
                    headers: this.contentHeader,
                    body: JSON.stringify(this.data),
            })
            .then(function(response) {
                return response.json();
            })
            .catch(error => console.log(error));
        }

        getCookiesData() {
            if (document.cookie && document.cookie !== '') {
                let cookies = document.cookie.split(';');
                for(let el of cookies) {
                    if(el.split('=')[0].replace(/\s/g, '') === "csrftoken") {
                        this.csrfToken = el.split('=')[1]
                    }
                }
            }
        }

    }

//        "email": "",
//    "password1": "",
//    "password2": "",
//    "first_name": "",
//    "date_of_birth": null

    let user = new Login();

