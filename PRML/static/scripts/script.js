Array.prototype.random = function () {
    let i = Math.floor(Math.random() * this.length);
    return [this[i], i];
};

const membership_types = ["None", "Silver", "Gold", "Platinum"];
const categories = ["Electronics", "Furniture", "Sports", "Travel", "Cloths"];
const products = [
    ["Laptop", "Smartphone", "Fridge", "TV", "AC", "Computer", "Cooler", "Speaker", "Tablet", "Heater"],
    ["Table", "Chair", "Cabinet", "Desk", "Cupboard", "Shelve", "Stand", "Soffa", "Bed", "Couch", "Bench"],
    ["Cricket_Bat", "Tennis_Ball", "Season_Ball", "Basket_Ball", "Football", "TT_Kit", "Cricket_Kit", "Javeline", "Baseball_Kit", "Hockey_Kit"],
    ["Bag", "Camping_Net", "Sleeping_Bag", "Stove", "Medical_Kit", "Stick", "Rope", "Tools_Kit"],
    ["TShirt", "Shirt", "Pant", "Joggers", "Hoodie", "Shoes", "Slippers", "Suit", "Half_Pant"],
];
const prices = [
    [450, 1200, 250, 1800, 300, 500, 400, 1500, 500, 1000, 1000, 3000, 400, 800, 400, 700, 500, 1500, 500, 900],
    [150, 200, 300, 350, 450, 500, 600, 650, 750, 800, 900, 950, 1050, 1100, 1200, 1250, 1350, 1400, 1500, 1550, 1600, 1650],
    [30, 40, 60, 70, 90, 100, 120, 130, 150, 160, 180, 200, 210, 220, 240, 250, 270, 280, 300, 320],
    [100, 120, 50, 80, 80, 100, 150, 200, 200, 250, 30, 40, 40, 60, 120, 150, 80, 100],
    [20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 60, 70, 80, 90, 100, 110],
];
const payment_methods = ["Cash", "Credit Card", "Debit Card", "EMI"];
const colors = ["Red", "Cyan", "Green", "Blue", "White", "Yellow", "Purple"];
const sizes = ["Small", "Medium", "Large", "XL", "XXL"];

function setup() {
    for (let j = 0; j < 5; j++) {
        let ec = document.getElementById(categories[j] + "_Container");
        for (let i = 0; i < 10; i++) {
            let prod = products[j].random();
            let col = colors.random();
            let sz = sizes.random();
            let price = randomInt(prices[j][prod[1]*2],prices[j][prod[1]*2 + 1]);

            let elem = makeElem();
            elem.querySelector("#title").innerHTML = prod[0].replaceAll('_', ' ');
            elem.querySelector("img").className = "prod-" + col[0].toLowerCase();
            elem.querySelector("p").innerHTML = `<b>Color :</b> ${col[0]}<br><b>Size :</b> ${sz[0]}<br><b>Price :</b> $${price}`;
            elem.querySelector("img").src = `../static/images/${prod[0]}.png`;

            ec.appendChild(elem);
        }
    }
}


function makeElem() {
    let elem = document.createElement("div");
    elem.className = "card m-1";
    elem.style = "width: 18rem;";
    elem.innerHTML = `
        <img style="width:15rem;height:15rem;" src="../static/images/Smartphone.png" class="card-img-top" alt="...">
        <div class="card-body">
            <h5 id="title" class="card-title">Card title</h5>
            <p class="card-text"></p>
            <a href="#" class="btn btn-primary">Buy</a>
        </div>
    `;
    return elem;
}
function randomInt(min, max) {
    return Math.floor(Math.random() * (max - min) + min);
}

function updatePage() {
    let data = udata['data'];
    let recom = udata['Recommendations'];
    document.querySelector('#uname').textContent = data['n'];
    document.querySelector('#recomCard').classList.remove("d-none");
    document.querySelector('#uimage').classList.remove("d-none");
    var cont = document.querySelector('#Recom_Container');
    for (let i = 0; i < 8; i++) {
        let elem = makeElem();
        let col = colors.random();
        let sz = sizes.random();
        let inds = findIn2d(recom[i]);
        let price = randomInt(prices[inds[0]][inds[1] * 2], prices[inds[0]][inds[1] * 2 + 1]);

        elem.querySelector("#title").innerHTML = recom[i].replaceAll('_',' ');
        elem.querySelector("img").className = "prod-" + col[0].toLowerCase();
        elem.querySelector("p").innerHTML = `<b>Color :</b> ${col[0]}<br><b>Size :</b> ${sz[0]}<br><b>Price :</b> $${price}`;
        elem.querySelector("img").src = `../static/images/${recom[i]}.png`;

        cont.appendChild(elem);
    }
}

function findIn2d(item) {
    let i = 0;
    for (let cat of products) {
        let j = 0;
        for (let prod of cat) {
            if (prod === item) return [i, j];
            j++;
        }
        i++;
    }
    return [-1, -1];
}

function updateProfilePage() {
    let data = udata['data'];
    document.querySelector('#uid').textContent = data['i'];
    document.querySelector('#uname').textContent = data['n'];
    document.querySelector('#email').textContent = data['e'];
    document.querySelector('#pn').textContent = data['p'];
    document.querySelector('#adrs').textContent = data['a'];
    document.querySelector('#dob').textContent = data['d'];
    document.querySelector('#gen').textContent = data['g'];
    document.querySelector('#memb').textContent = data['m'];
    document.querySelector('#fav').textContent = data['f'];
    document.querySelector('#llogin').textContent = data['l'];
    document.querySelector('#lpur').textContent = data['x'];
}

function setCookie(name, value, days) {
    let expires = "";
    if (days) {
        let date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + value + expires + "; path=/";
}

function getCookie(name) {
    let cookies = document.cookie.split('; ');
    for (let cookie of cookies) {
        let [key, value] = cookie.split('=');
        if (key === name) {
            return value;
        }
    }
    return null;
}