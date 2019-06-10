class Basket {
        constructor() {
            this.dataProducts = [];
            this.content = '';
            this.csrftoken = '';
            this.price = 0;
            this.API = `${window.location.origin}/api/v1/basket/`;
            this.init();
        }

        init() {
            this.getCSRFToken();
            this.requestProductsGet();
        }

        requestProductsGet() {
            fetch(this.API)
                .then(function (response) {
                    return response.json();
                })
                .then(data => {
                    this.dataProducts = data.results;
                })
                .then(data => {
                    this.renderBasketItems();               // отоюражение содержимого корзины
                    this.setHandlerChangeInNumber();        // обработчик ввода количества товаров
                    this.setHandlerChangeCloseBtn();        // обработчик удаления товара из корзины
                    let product_like = new ProductLike(this.csrftoken);   // отображение избранное в товарах
                })
                .catch(error => console.log(error));
        }

        // отображение содержимого корзины
        renderBasketItems() {
            for (let elem of this.dataProducts) {
                this.price += +elem.price * elem.quantity * (100 - elem.discount) / 100;
                this.content += this.getHtmlBasketUnit(elem);
            }

            this.content += `
                        <div class="total-amount">
                            Всего <span>${this.price}</span> руб.
                        </div>
                        `

            const block = document.createElement('div');
            block.innerHTML = this.content;
            document.querySelector('.basket .basket-items').appendChild(block);
            document.querySelector('.basket .basket-order .total-cost').innerText =
                `${this.price + +document.querySelector('.basket .delivery-price').dataset.price} руб.`;
        }

        getHtmlBasketUnit(elem) {
            return `
                <div id="${elem.id}">
                    <div class="basket-unit d-flex" >
                        <div class="img">
                        <a href="${elem.product_url.replace('/api/v1/', '/')}">
                            <img src="${elem.main_img}"
                                 alt="${elem.name_product}" height="150">
                        </a>

                        </div>
                        <div class="basket-unit-description">
                            <div class="price">Цена: <span>${+elem.price * (100 - elem.discount) / 100} руб.</span></div>
                            <div class="name">Название:
                                <span>${elem.name_category} ${elem.logotype}</span></div>
                            <div class="name">Цвет: <span>${elem.color}</span></div>
                            <div class="d-sm-flex code-size-count">
                                <div>
                                    Код: <span>${elem.article}</span>
                                </div>
                                <div class="size-count">
                                    Размер: <span>${elem.size}</span>
                                </div>
                                <div class="size-count">
                                    Кол-во: <span><input type="number" min="1"
                                                         data-product_by_size_id = ${elem.product_by_size_id}
                                                         data-id = ${elem.id}
                                                         data-product_quantity = ${elem.quantity}
                                                         value=${elem.quantity}>
                                            </span>
                                </div>
                            </div>
                            <button data-like=${false} data-article=${elem.article} data-product_id=${elem.product_id}>
                                <i class="far fa-heart"></i> Добавить в избранное
                            </button>
                        </div>
                        <button class="close-btn ml-auto" data-id = ${elem.id}
                                                  data-price = ${+elem.price * elem.quantity * (100 - elem.discount) / 100}>
                            <i class="far fa-times" data-id = ${elem.id}
                                                    data-price = ${+elem.price * elem.quantity * (100 - elem.discount) / 100}>
                            </i>
                        </button>
                    </div>
                    <hr>
                </div>
            `
        }

        // обработчик события ввода количества товаров
        setHandlerChangeInNumber() {
            let elements = document.querySelectorAll('.basket-unit .code-size-count .size-count input');
            for(let el of elements) {
                el.onchange = (event) => {
                    this.objInputNumber = event.target;
                    this.requestPut();                  // запрос на изменение количества  определленного товара в корзине
                }
            }
        }

        // обработчик события удаления товара из корзины
        setHandlerChangeCloseBtn() {
            let elements = document.querySelectorAll('.basket .basket-items .close-btn');

            for(let el of elements) {
                el.onclick = (event) => {
                    this.objBtnClose = event.target;
                    this.requestDelete();
                }
            }
        }

        // запрос на изменение количества товара в корзине
        requestPut() {
            fetch(`${this.API + this.objInputNumber.dataset.id}/`, {
                method: 'PUT',
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": this.csrftoken,
                },
                body: JSON.stringify({
                   "product_by_size_id": this.objInputNumber.dataset.product_by_size_id,
                   "quantity": this.objInputNumber.value
                })
            })
            .then(function (response) {
                return response.json();
            })
            .then(data => {
                if (data.id) {
                    this.renderPriceProductsPut(data);     // если запрос успешен, изменение отображения стоимости на странице
                }
            })
            .catch(error => console.log(error));
        }

        // запрос на удаление товара из корзины
        requestDelete() {
            fetch(`${this.API + this.objBtnClose.dataset.id}/`, {
                method: 'DELETE',
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": this.csrftoken,
                },
                body: JSON.stringify({})
            })
            .then(() => {
                this.renderPriceProductsDelete();       // изменение стоимости на странице
                this.renderProductDelete();             // удаление товара со страницы
            })
            .catch(error => console.log(error));
        }

        // отображения стоимости на странице
        renderPriceProductsPut(data) {
            let price_product = +data.price * this.objInputNumber.value * (100 - data.discount) / 100;
            document.getElementById(this.objInputNumber.dataset.id).querySelector('.close-btn').dataset.price = price_product;
            document.getElementById(this.objInputNumber.dataset.id).querySelector('.close-btn i').dataset.price = price_product;

            this.price += +data.price * (this.objInputNumber.value - this.objInputNumber.dataset.product_quantity) * (100 - data.discount) / 100;
            this.objInputNumber.dataset.product_quantity = this.objInputNumber.value;

            document.querySelector('.basket .basket-items .total-amount span').innerText = this.price;
            document.querySelector('.basket .basket-order .total-cost').innerText =
                `${this.price + +document.querySelector('.basket .delivery-price').dataset.price} руб.`;
        }


        // отображения стоимости на странице
        renderPriceProductsDelete() {
            this.price -= this.objBtnClose.dataset.price;

            document.querySelector('.basket .basket-items .total-amount span').innerText = this.price;
            document.querySelector('.basket .basket-order .total-cost').innerText =
                `${this.price + +document.querySelector('.basket .delivery-price').dataset.price} руб.`;
        }

        // удаление товара на странице из корзины
        renderProductDelete() {
            document.getElementById(this.objBtnClose.dataset.id).remove();
        }

        getCSRFToken() {
                if (document.cookie && document.cookie !== '') {
                    let cookies = document.cookie.split(';');
                    for (let el of cookies) {
                        if (el.split('=')[0].replace(/\s/g, '') === "csrftoken") {
                            this.csrftoken = el.split('=')[1];
                        }
                    }
                }
            }
    }




    class ProductLike {
            constructor(csrftoken) {
                this.productsList = [];
                this.API = `${window.location.origin}/api/v1/like/`;
                this.csrftoken = csrftoken;
                this.init();
            }

            init() {
                this.requestProductsLike();     // запрос списка избранных товаров
                this.clickProductsLike();       // установка обработчика на кнопку добавление в избранное
            }

            requestProductsLike() {
                fetch(`${this.API}`)
                    .then(function (response) {
                        return response.json();
                    })
                    .then(data => {
                        this.productsLikeList = data.results;
                    })
                    .then(() => {
                        this.productsLike();            // отображение маркера избранный товар
                    })
                    .catch(error => console.log(error));
            }

            // запрос на добавление товара в избранное
            requestPost(id, article) {
                fetch(this.API, {
                    method: 'POST',
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": this.csrftoken,
                    },
                    body: JSON.stringify({
                            "product_id": id,
                        }
                    )
                })
                    .then(function (response) {
                        return response.json();
                    })
                    .then(data => {
                        if (data.id) {
                            this.addStyleButtonLike(article);   // отражение маркера избранный товар
                        }
                    })
                    .catch(error => console.log(error));
            }

            // запрос на удаление товара из избранного
            requestDelete(id, article) {
                fetch(`${this.API + id}/`, {
                    method: 'DELETE',
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": this.csrftoken,
                    },
                })
                    .then(function (response) {
                        return response;
                    })
                    .then(data => {
                        if (!data.id) {
                            this.removeStyleButtonLike(article);    // удаление маркера избранный товар
                        }
                    })
                    .catch(error => console.log(error));
            }


            // отображение маркера избранный товар в товарах корзины
            productsLike() {
                for (let el of this.productsLikeList) {
                    this.addStyleButtonLike(el.article);
                }
            }

            // установка события на кнопку добавления товара в избранное
            clickProductsLike() {
                let btnAddProductsLike = document.querySelectorAll('.basket-items .basket-unit-description > button');
                for (let el of btnAddProductsLike) {
                    el.onclick = (event) => {
                        if (event.target.dataset.like === 'true') {
                            this.requestDelete(event.target.dataset.product_id, event.target.dataset.article);
                        } else {
                            this.requestPost(event.target.dataset.product_id, event.target.dataset.article);
                        }
                    }
                }
            }

            // добавление маркера избранный товар
            addStyleButtonLike(article) {
                for (let el of document.querySelectorAll(`[data-article=${article}]`)) {
                    el.innerHTML = '<i class="far fa-heart"></i>Удалить из избранного';
                    el.style.backgroundColor = '#f92672';
                    el.style.color = '#ffffff';
                    el.dataset.like = true;
                };

            }

            // удаление маркера избранный товар
            removeStyleButtonLike(article) {
                for (let el of document.querySelectorAll(`[data-article=${article}]`)) {
                    el.innerHTML = '<i class="far fa-heart"></i>Добавить в избранное';
                    el.style.backgroundColor = '#ffffff';
                    el.style.color = '#383838';
                    el.dataset.like = false;
                };
            }
    }

    class Delivery {
        constructor() {
            this.deliverPrice = 0;
            this.changeInputDelivery();
        }

        changeInputDelivery() {
            let block = document.querySelector('.basket .basket-order .form-control');
            block.onchange = () => {
                this.deliverPrice = block.options[block.selectedIndex].value;
                this.renderPriceDeliver();
            }
        }

        renderPriceDeliver() {
            document.querySelector('.basket .basket-order .sum .delivery-price').innerText = `${this.deliverPrice} руб.`;
            document.querySelector('.basket .basket-order .total-cost').innerText =
                `${basketProducts.price + +this.deliverPrice} руб.`;
        }

    }

    let delivery = new Delivery();
    let basketProducts = new Basket();