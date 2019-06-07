class Login {
    constructor() {
        this.login = false;
//            this.email = '';
//            this.password = '';
        this.data = {};
        this.contentHeader = {};
        this.modalTitle = document.querySelector('.modal-login .modal-title');
        this.button = document.querySelector('.modal-login .modal-footer .login-btn');
        this.URL = `${window.location.origin}/api/v1/`;
        this.API = '';
        // проверка залогинен пользователь или нет
        this.getIsLogin();
    }

    init() {
        // получение CSRF токена
        this.getCookiesData();
        // отрисовка модального окна в зависимости залогинен пользователь или нет
        this.renderModalLoginForm();
        // установка обработчика событий на кнопку "ВОЙТИ"
        this.onclickLogin();
        // При закрытии модального окна перезапуск
        document.querySelector('.modal-login .modal-header .close').onclick = () => {
            this.init();
        };
        // при нажатии на кнопку "РЕГИСТРАЦИЯ" переходим к регистрации
        document.querySelector('.modal-login .modal-footer .render_registration_modal').onclick = () => {
            if (document.querySelector('.modal-login .modal-body p')) {
                // если выводилось предупреждение убираем его
                document.querySelector('.modal-login .modal-body p').remove();
            }
            new Register();
        }
    }

    // проверка залогинен пользователь или нет
    getIsLogin() {
        fetch(`${this.URL}user/`)
            .then(function (response) {
                return response.json();
            })
            .then(data => {
                if (data.detail === "Authentication credentials were not provided.") {
                    this.login = false;
                }
                if (data.email) {
                    this.login = true;
                }
                this.init()
            })
            .catch(error => console.log(error));
    }

    // отрисовка модального окна в зависимости залогинен пользователь или нет
    renderModalLoginForm() {
        if (document.querySelector('.modal-login .modal-body p')) {
            // если выводилось предупреждение убираем его
            document.querySelector('.modal-login .modal-body p').remove();
        }

        if (this.login) {
            // пользователь залогинен
            document.querySelector('.modal-login .render_registration_modal').style.display = 'none'; // убираем кнопку перхода к регистрации
            document.querySelector('.modal-login .request_registration').style.display = 'none';      // убираем кнопку отправления формы регистрации
            document.querySelector('.modal-login .modal-body').style.display = 'none';                // убираем поля ввода данных
            document.querySelector('.modal-login .registration-by-vk').style.display = 'none';        // убираем кнопку регистрации через VK
            document.querySelector('.modal-login .registration-by-github').style.display = 'none';    // убираем кнопку регистрации через GITHUB

            document.querySelector('#basket-button').style.display = 'block';        // вывод значка "корзины"
            document.querySelector('#like-button').style.display = 'block';          // вывод значка "избранное"
            document.querySelector('#non-logged-in').style.display = 'none';
            document.querySelector('#non-logged-in').style.position = 'absolute';
            document.querySelector('#logged-in').style.display = 'block';
            document.querySelector('#logged-in').style.position = 'static';

            this.button.innerText = 'Выйти';                    // надпись на кнопке "Выйти"
            this.modalTitle.innerText = 'Выйти с сайта';        // надпись заголовка "Выйти с сайта"
        } else {
            // пользователь НЕ залогинен
            document.querySelector('.modal-login .modal-body').style.display = 'block';                 // вывести поля ввода данных
            document.querySelector('.modal-login .password_2').style.display = 'none';                  // убираем поле ввода подтверждение пароля
            document.querySelector('.modal-login .first_name').style.display = 'none';                  // убираем поле ввода имени
            document.querySelector('.modal-login .date_of_birth').style.display = 'none';               // убираем поле ввода даты рождения

            document.querySelector('.modal-login .render_registration_modal').style.display = 'block';  // вывод кнопки перехода к регистрации
            document.querySelector('#loginOkButton').style.display = 'block';                           // вывод кнопки "Входа"
            document.querySelector('.modal-login .request_registration').style.display = 'none';        // убрать кнопку отправки формы регистрации
            document.querySelector('.modal-login .registration-by-vk').style.display = 'block';         // вывести кнопку регистрации через VK
            document.querySelector('.modal-login .registration-by-github').style.display = 'block';     // вывести кнопку регистрации через GITHUB

            document.querySelector('#defaultForm-email').classList.add('validate');
            document.querySelector('#defaultForm-pass-1').classList.add('validate');

            document.querySelector('#basket-button').style.display = 'none';        // убрать значок "корзины"
            document.querySelector('#like-button').style.display = 'none';          // убрать значок "избранное"
            document.querySelector('#non-logged-in').style.display = 'block';
            document.querySelector('#non-logged-in').style.position = 'static';
            document.querySelector('#logged-in').style.display = 'none';
            document.querySelector('#logged-in').style.position = 'absolute';

            this.button.innerText = 'Войти';                    // надпись на кнопке "Войти"
            this.modalTitle.innerText = 'Войти на сайт';        // надпись заголовка "Войти с сайта"
        }
    }

    // установка обработчика событий на кнопку "ВОЙТИ"
    onclickLogin() {
        // const block = document.querySelector('.modal-login .modal-footer .login-btn');
        this.button.onclick = () => {
            // получение данных для запроса на вход или выход
            this.getDataLogin();
            // отправка запроса входа/выхода на сервер
            this.requestLogin();
        };
    }

    // получение данных для запроса на вход или выход
    getDataLogin() {
        if (this.login) {
            this.API = `${this.URL}logout/`;
            this.contentHeader = {
                "Content-Type": "application/json",
                "X-CSRFToken": this.csrfToken,
            };
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

    // отправка запроса входа/выхода на сервер
    requestLogin() {
        fetch(this.API, {
            method: 'POST',
            headers: this.contentHeader,
            body: JSON.stringify(this.data),
        })
            .then(function (response) {
                return response.json();
            })
            .then(data => {
                console.log('LOGIN ---> ', data);

                if (data.detail === "Successfully logged out.") {
                    // если выход прошел успешно
                    document.querySelector('.modal-login .modal-header .close').click();    // закрытие модального окна
                    this.login = false;                                                     // пользователь вышел
                    this.init();                                                            // перезапуск
                } else if (data.key) {
                    // если вход прошел успешно
                    if (this.blockError) {
                        // усли выводилось сообщение с предупреждением
                        this.blockError.remove();       // удаление сообщеня с предупреждением
                    }
                    document.querySelector('.modal-login .modal-header .close').click();    // закрытие модального окна
                    this.login = true;                                                      // пользователь вошел
                    this.init();
                } else if (data.non_field_errors && data.non_field_errors[0] === "E-mail is not verified.") {
                    // если адрес электронной почты не подтвержден
                    this.login = false;                                                     // пользователь вышел
                    this.renderErrorLogin('Подтвердите адрес электронной почты.');          // вывод предупреждения
                } else {
                    // если при входе/выходе возникла ошибка
                    this.renderErrorLogin('Введены неверные учетные данные!');              // вывод предупреждения
                    this.login = false;                                                     // пользователь вышел
                }
            })
            .catch(error => console.log(error));
    }

    // вывод предупреждения
    renderErrorLogin(content) {
        if (document.querySelector('.modal-login .modal-body p')) {
            // усли выводилось сообщение с предупреждением
//                document.querySelector('.modal-login .modal-body p').innerText = content;       // изменение текста предупреждением
            document.querySelector('.modal-login .modal-body p').innerText = content;                                            // изменение текста предупреждением
        } else {
            this.blockError = document.createElement('p');
            this.blockError.style.color = 'red';
            this.blockError.style.fontWeight = 'bold';
            this.blockError.innerText = content;
            document.querySelector('.modal-login .modal-body').insertAdjacentElement('afterbegin', this.blockError);
        }


    }

    // получение CSRF токена
    getCookiesData() {
        if (document.cookie && document.cookie !== '') {
            let cookies = document.cookie.split(';');
            for (let el of cookies) {
                if (el.split('=')[0].replace(/\s/g, '') === "csrftoken") {
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
        // this.csrfToken;
        this.API = '';
        this.modalTitle = document.querySelector('.modal-login .modal-title');
        this.URL = `${window.location.origin}/api/v1/`;
        this.getCookiesData();
        this.init();
    }

    init() {
        this.clickButtonClose();                            // установка обработчика события на кнопку закрытия модального окна
        this.renderFormRegistration();                      // отрисовка формы для регистрации
        Register.deleteClassValidate();
        this.clickRequestRegistration();                    // отправка формы регистрации
        this.validationFieldOff();
    }

    // отрисовка формы регистрации
    renderFormRegistration() {
        for (let el of document.querySelectorAll('.md-form')) {
            // увеличение отступов между полями ввода
            el.style.marginTop = '3.0rem';
        }

        this.modalTitle.innerText = 'Регистрация';                                                    // вывод в заголовке "Регистрация"

        document.querySelector('.modal-login .modal-body').style.display = 'block';                     // вывод полей регистрации
        document.querySelector('.modal-login .password_2').style.display = 'block';                     // вывод поля подтверждения пароля
        document.querySelector('.modal-login .first_name').style.display = 'block';                     // вывод поля ввода имени
        document.querySelector('.modal-login .date_of_birth').style.display = 'block';                  // вывод поля даты рождения

        document.querySelector('.modal-login .render_registration_modal').style.display = 'none';       // сокрытие кнопки перехода к регистрации
        document.querySelector('.modal-login .request_registration').style.display = 'block';           // вывод кнопки отправки формы регистрации

        document.querySelector('.modal-login #loginOkButton').style.display = 'none';                   // сокрытие кнопки входа
        document.querySelector('.modal-login .registration-by-vk').style.display = 'block';             // вывод кнопки регистрации через VK
        document.querySelector('.modal-login .registration-by-github').style.display = 'block';         // вывод кнопки регистрации через GITHUB
    }

    static deleteClassValidate() {
        document.querySelector('#defaultForm-email').classList.remove('validate');
        document.querySelector('#defaultForm-email').classList.remove('valid');
        document.querySelector('#defaultForm-pass-1').classList.remove('validate');
        document.querySelector('#defaultForm-pass-1').classList.remove('valid');
        document.querySelector('#defaultForm-pass-2').classList.remove('validate');
        document.querySelector('#defaultForm-first_name').classList.remove('validate');
        document.querySelector('#defaultForm-date_of_birth').classList.remove('validate');
    }

    // // проверка валидности паролей
    // validatePasDuplicate() {
    //     // установка обработчика события на поле второго пароля
    //     document.querySelector('#defaultForm-pass-2').onchange = () => {
    //         let passwordDuplicate = document.querySelector('#defaultForm-pass-2');
    //         let pass1 = document.querySelector('#defaultForm-pass-1').value;            // получение первого пароля
    //         let pass2 = document.querySelector('#defaultForm-pass-2').value;            // получение второго пароля
    //
    //         if (pass1 === pass2) {
    //             // если пароли одинаковы
    //             passwordDuplicate.classList.remove('invalid');                          // удаление класса выводящего сообщение "Не верно"
    //             passwordDuplicate.classList.add('valid');                               // выделение поля второго пароля зеленым и сообщения "Верно"
    //         } else {
    //             passwordDuplicate.classList.remove('valid');                            // удаление класса выводящего сообщение "Верно"
    //             passwordDuplicate.classList.add('invalid');                             // выделение поля второго пароля красным и вывод сообщения "Не верно"
    //         }
    //     }
    // }
    //
    // // проверка поля ввода даты рождения
    // validateDataBirth() {
    //     let dateBirth = document.querySelector('#defaultForm-date_of_birth');
    //
    //     dateBirth.onchange = () => {
    //         if (document.querySelector('#defaultForm-date_of_birth').value) {
    //             dateBirth.classList.remove('invalid');
    //             dateBirth.classList.add('valid');
    //         } else {
    //             dateBirth.classList.remove('valid');
    //             dateBirth.classList.add('invalid');
    //         }
    //     }
    // }

    // отправка формы регистрации
    clickRequestRegistration() {
        // установка события на кнопку "регистрации"
        document.querySelector('.modal-login .modal-footer .request_registration').onclick = () => {
            this.getDataRegister();                                                             // получение данных для отправки формы

            document.querySelector('#defaultForm-email').style.borderColor = '#ced4da';
            document.querySelector('#defaultForm-pass-1').style.borderColor = '#ced4da';
            document.querySelector('#defaultForm-pass-2').style.borderColor = '#ced4da';
            document.querySelector('#defaultForm-first_name').style.borderColor = '#ced4da';
            document.querySelector('#defaultForm-date_of_birth').style.borderColor = '#ced4da';
            console.log('data', this.data);

            if (!Register.validateEmail(this.data['email'])) {
                // если email не валиден
                console.log('Введите правильный E-MAIL.');
                document.querySelector('#defaultForm-email').style.borderColor = '#f44336';
                this.renderErrorRegistration('Введите правильный E-MAIL.');                     // вывот предупреждения
            } else if (this.data['password1'] !== this.data['password2']) {
                // если пароли не совпадают
                console.log('Пароли не совпадают.');
                document.querySelector('#defaultForm-pass-2').style.borderColor = '#f44336';
                this.renderErrorRegistration('Пароли не совпадают.');                           // вывод предупреждения
            } else if (this.data['password1'] && !Register.validatePassword(this.data['password1'])) {
                console.log('Пароли меньше 8 символов.');
                document.querySelector('#defaultForm-pass-1').style.borderColor = '#f44336';
                this.renderErrorRegistration('Пароль должен содержать не менее 8 символов.');
            } else if (!this.data['first_name']) {
                // если не введено имя
                console.log('Введите имя');
                document.querySelector('#defaultForm-first_name').style.borderColor = '#f44336';
                this.renderErrorRegistration('Введите имя.');                                   // вывод предупреждения
            } else if (!this.data['date_of_birth'] || !Register.validateDataBirth(this.data['date_of_birth'])) {
                // если дата рождения не введена
                console.log('Введите правильную дату рождения.');
                document.querySelector('#defaultForm-date_of_birth').style.borderColor = '#f44336';
                this.renderErrorRegistration('Введите правильную дату рождения.');              // вывод предупреждения
            } else {
                this.requestRegister();                                                         // отправка формы регистрации
            }
        }
    }


    // получение данных для отправки формы регистрации
    getDataRegister() {
        this.API = `${this.URL}registration/`;
        this.contentHeader = {
            "Content-Type": "application/json",
            "X-CSRFToken": this.csrfToken,
        };
        this.data = {
            "email": document.querySelector('#defaultForm-email').value,
            "password1": document.querySelector('#defaultForm-pass-1').value,
            "password2": document.querySelector('#defaultForm-pass-2').value,
            "first_name": document.querySelector('#defaultForm-first_name').value,
            "date_of_birth": document.querySelector('#defaultForm-date_of_birth').value,
        };
    }

    // отправка формы регистрации
    requestRegister() {
        fetch(this.API, {
            method: 'POST',
            headers: this.contentHeader,
            body: JSON.stringify(this.data),
        })
            .then(function (response) {
                return response.json();
            })
            .then(data => {
                console.log('REGISTRATION ---> ', data);
                if (document.querySelector('.modal-login .modal-body p')) {
                    // если выведено предупреждение
                    document.querySelector('.modal-login .modal-body p').remove();      // удаление предупреждения
                }

                if (data.detail && data.detail === 'Verification e-mail sent.') {
                    // если регистрация прошла успешно
                    console.log('Подтверждение отправлено по электронной почте.', data);
                    document.querySelector('.modal-login .modal-title').innerText = 'Подтверждение отправлено по электронной почте'; // вывод соощения об успешной регистрации
                    Register.renderModalVerification();                                     // отрисовка содержимого модального окна при удачной регистрации
                    this.clickRequestRegistration();
                } else if (data.email && data.email[0] === 'A user is already registered with this e-mail address.') {
                    // если пользователь с таким email уже существует
                    console.log('Пользователь c введенным адресом электронной почты уже зарегистрирован.', data);
                    this.renderErrorRegistration('Пользователь c введенным адресом электронной почты уже зарегистрирован.');    // вывод предупреждения
                    this.clickRequestRegistration();                                                                                                // перезапуск
                } else {
                    this.renderErrorRegistration('Ошибка регистрациию. Попробуйте зарегистрироваться позже.');
                    this.clickRequestRegistration();
                }
                console.log('Ответ от бэка ', data)
            })
            .catch(error => console.log(error));
    }

    // отрисовка содержимого модального окна при удачной регистрации
    static renderModalVerification() {
        document.querySelector('.modal-login .modal-body').style.display = 'none';                              // сокрытие полей регистрации
        document.querySelector('.modal-login .modal-footer .request_registration').style.display = 'none';      // сокрытие кнопки регистрация
    }

    // обработчик события закрытия окна
    clickButtonClose() {
        document.querySelector('.modal-login').onhide = () => {
            user.init();                                                   // вызов инициализации класса Login
        }

    }

    // отрисовка предупреждения
    renderErrorRegistration(content) {
        console.log('отрисовка предупреждения', content);
        if (document.querySelector('.modal-login .modal-body p')) {
            // если предупреждение уже выведено
            document.querySelector('.modal-login .modal-body p').innerText = content;                           // изменение содержимого предупреждения

        } else {
            this.blockError = document.createElement('p');
            this.blockError.style.color = 'red';
            this.blockError.style.fontWeight = 'bold';
            this.blockError.innerText = content;
            document.querySelector('.modal-login .modal-body').insertAdjacentElement('afterbegin', this.blockError);
        }
    }

    validationFieldOff() {
        document.querySelector('#defaultForm-email').onfocus = () => {
            document.querySelector('#defaultForm-email').style.borderColor = '#ced4da';
        };
        document.querySelector('#defaultForm-pass-1').onfocus = () => {
            document.querySelector('#defaultForm-pass-1').style.borderColor = '#ced4da';
        };
        document.querySelector('#defaultForm-pass-2').onfocus = () => {
            document.querySelector('#defaultForm-pass-2').style.borderColor = '#ced4da';
        };
        document.querySelector('#defaultForm-first_name').onfocus = () => {
            document.querySelector('#defaultForm-first_name').style.borderColor = '#ced4da;';
        };
        document.querySelector('#defaultForm-date_of_birth').onfocus = () => {
            document.querySelector('#defaultForm-date_of_birth').style.borderColor = '#ced4da';
        }
    }

    // получение CSRF токена
    getCookiesData() {
        if (document.cookie && document.cookie !== '') {
            let cookies = document.cookie.split(';');
            for (let el of cookies) {
                if (el.split('=')[0].replace(/\s/g, '') === "csrftoken") {
                    this.csrfToken = el.split('=')[1]
                }
            }
        }
    }

    static validateEmail(email) {
        return /^([a-z0-9_.-]+)@([a-z0-9_.-]+)\.([a-z.]{2,6})$/.test(String(email));
    }

    static validatePassword(pass) {
        return /^\S{8,}$/.test(String(pass));
    }

    static validateDataBirth(date) {
        return /^((19[0-9][0-9])|(20[0-1][0-9]))-((0[1-9])|(1[0-2]))-((0[1-9])|(1[0-9])|(2[0-9])|(3[0-1]))$/.test(String(date));
    }
}

let user = new Login();