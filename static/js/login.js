    class Login {
        constructor() {
            this.login = false;
            this.email = '';
            this.password = '';
            this.data = {};
            this.contentHeader = {};
            this.modalTitle = document.querySelector('.modal-title');
            this.button = document.querySelector('.modal-footer .login-btn');
            this.URL = `${window.location.origin}/api/v1/`;
            this.API = '';
            this.getIsLogin();
        }

        init() {

            this.getCookiesData();
            this.renderModalLoginForm();
            this.onclickLogin();
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
                this.init();
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

        renderModalLoginForm() {
            if (this.login) {
                document.querySelector('.modal-body').style.display = 'none';
                document.querySelector('#basket-button').style.display = 'block';
                document.querySelector('#like-button').style.display = 'block';
                this.button.innerText = 'Выйти';
                this.modalTitle.innerText = 'Выйти с сайта';
            }
            else {
                document.querySelector('.modal-body').style.display = 'block';
                document.querySelector('#basket-button').style.display = 'none';
                document.querySelector('#like-button').style.display = 'none';
                this.button.innerText = 'Войти';
                this.modalTitle.innerText = 'Войти на сайт';
            }
        }


        getData() {
            this.email = document.getElementById('defaultForm-email').value;
            this.password = document.getElementById('defaultForm-pass').value;

            if (this.login) {
                this.API = `${this.URL}logout/`;
                this.data = {};
                this.contentHeader = {"Content-Type": "application/json", "X-CSRFToken": this.csrfToken,};
            } else {
                this.API = `${this.URL}login/`;
                this.data = {"email": this.email, "password": this.password};
                this.contentHeader = {"Content-Type": "application/json",};
            }
        }

        onclickLogin() {
            const block = document.querySelector('.modal-footer .login-btn');
            block.onclick = () => {
                this.getData();
                this.requestLogin();
            };
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
                    document.querySelector('.modal-header .close').click();
                    this.login = false;
                    this.init();
                }
                if (data.key) {
                    if (this.blockError){
                        this.blockError.remove();
                    }
                    this.login = true;
                    this.init();
                    document.querySelector('.modal-header .close').click()
                }
                else if (data.detail && data.detail === "Successfully logged out.") {
                    document.querySelector('.modal-header .close').click();
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
//                else if (data.email && data.email[0] === "Enter a valid email address.") {
//                    if (!this.blockError){
//                        this.renderErrorLogin();
//                    }
//                    this.login = false;
//                    this.init();
//                }
//                else if (data.non_field_errors && data.non_field_errors[0] === "Unable to log in with provided credentials.") {
//                    if (!this.blockError){
//                        this.renderErrorLogin();
//                    }
//                    this.login = false;
//                    this.init();
//                }
            })
            .catch(error => console.log(error));
        }

         renderErrorLogin() {
            this.blockError = document.createElement('p');
            this.blockError.style.color = 'red';
            this.blockError.style.fontWeight  = 'bold';
            this.blockError.innerText = 'Введены неверные учетные данные!';
            document.querySelector('.modal-body').insertAdjacentElement('afterbegin', this.blockError);
        }

    }
    let user = new Login();