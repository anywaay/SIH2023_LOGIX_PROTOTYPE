const express = require("express");
const bodyParser = require("body-parser");
const ejs = require("ejs");
const fs = require('fs');
const XLSX = require('xlsx');
// const { exec } = require('child_process');

const path = require('path');
var request = require('request-promise'); 
const { url } = require("inspector");

const app = express();
app.use(express.json());
app.use(express.static("public"));
app.set("view engine", "ejs");
app.use(bodyParser.urlencoded({extended: true}));

var accname = "Sign Up";
var accicon = "fa-regular fa-user";
var linkarr = [];
var finallink = "https://mkp.gem.gov.in/laptop-notebook/hp-247-g8-ryzen3-athlon-3045b-win11h-8133/p-5116877-32989524800-cat.html#variant_id=5116877-32989524800";
var flagg = 0;

var flipfinallink;

// product details variables
var proimage1;
var proimage2;
var proimage3;
var proname;
var promodel;
var probrand; 
var prostock;
var prominqty;
var pro_id;
var proorigin;
var proprice;
var pro_pricefor;
var pro_sellertype;
var pro_sellervari;
var prorating;
var sellerlink;
var proprocessordesc; 
var prographictype;
var prographicdesc;
var prooperatingsys;
var proramtype;
var proramsize;
var proramspeed;
var prohddsize; 
var prossdsize;
var prodisplay;
var prodisplayreso;
var prowarranty;

var laptoptrue;

var fliplink;
var flipprice;
var flipname;


var fliptitle;
var flipprobrand;
var flipproname;
var flipprogen;
var flipramsize;
var flipramtype;
var flipscreensize;
var flipscreenpixel;
var flipssdsize;
var flipwarranty;
var flipgraphics;


var ebayprice;
var ebayname;
var ebaylink;
var ebayrating;
var fliprating;
app.get("/", function(req, res){
    // res.render("index", {accountname: accname, accounticon: accicon});

        res.render("index", {
            accountname: accname,
            accounticon: accicon,
            searchingtitle: searchingTitle,
            cards: cardS,
            Flagg: flagg,
            flipArr: fliparr,
            ebayArr: ebayarr,
            flipRatingarr: flipratingarr,
            ebayRatingarr: ebayratingarr
        });
        
        flagg = 0;
        // searchingTitle = "Get the pricing and comparison details of your searched product right here!";

});

app.get("/login", function(req, res){
    res.render("login");
});
app.get("/signup", function(req, res){
    res.render("signup");
});
app.get("/about", function(req, res){
    res.render("about",{accountname: accname, accounticon: accicon});
});

app.get("/sellerdetails", function(req, res){
    res.render("seller_details", {accountname: accname, accounticon: accicon});
});

app.post("/login", function(req, res){

    var name = req.body.accName;
    var emailid = req.body.email;
    var password = req.body.pass;
    var userstate = req.body.state;
    console.log(userstate)
    
    accname = name
    accicon = "fa-solid fa-user";
    res.redirect("/");

});
app.post("/signup", function(req, res){
    var newname = req.body.newName;
    var newemailid = req.body.newemail;
    var newpassword = req.body.newpass;
    var newState = req.body.newstate;
    console.log(newState)
    
    accname = newname
    accicon = "fa-solid fa-user";
    res.redirect("/");

});

app.get("/product_details", function(req, res){

    res.render("product_details",{
        accountname: accname,
        accounticon: accicon,
        proImage1: proimage1,
        proImage2: proimage2,
        proImage3: proimage3,
        pro_Pricefor: pro_pricefor,
        proPrice: proprice,
        proStock: prostock,
        proMinqty: prominqty,
        proId: pro_id,
        proOrigin: proorigin,
        proSellertype: pro_sellertype,
        proSellervari: pro_sellervari,
        proRating: prorating,
        sellerLink: sellerlink,
        proName: proname,
        proModel: promodel,
        proBrand: probrand,
        proProcessordesc: proprocessordesc,
        proGraphictype: prographictype,
        proGraphicdesc: prographicdesc,
        proOperatingsys: prooperatingsys,
        proRamsize: proramsize,
        proRamtype: proramtype,
        proSsdsize: prossdsize,
        proHddsize: prohddsize,
        proDisplay: prodisplay,
        proDisplayreso: prodisplayreso,
        proWarranty: prowarranty,
        laptopTrue: laptoptrue,
        FlipLink: fliplink,
        FlipPrice: flipprice,
        flipTitle: fliptitle,
        flipproBrand: flipprobrand,
        flipproName: flipproname,
        flipproGen: flipprogen,
        flipramSize: flipramsize,
        flipramType: flipramtype,
        flipscreenSize: flipscreensize,
        flipscreenPixel: flipscreenpixel,
        flipssdSize: flipssdsize,
        flipWarranty: flipwarranty,
        flipGraphics: flipgraphics,
        ebayLink: ebaylink,
        ebayName: ebayname,
        ebayPrice: ebayprice
    });
});

    // function for detail page script parsing
    async function arraysum() { 
        console.log(finalsellerlink);
        var data = { 
            array: [finallink,
            "https://www.amazon.com/HP-Display-i3-1215U-Graphics-15-dy5599nr/dp/B0BVD8LZQL/ref=pd_aw_ci_mcx_pspc_dp_m_m_t_3?pd_rd_w=CSqNA&content-id=amzn1.sym.8601bd6b-5f84-4e74-9236-bbdc6b94ed42&pf_rd_p=8601bd6b-5f84-4e74-9236-bbdc6b94ed42&pf_rd_r=KCYGXQAEB84X82VS0MAF&pd_rd_wg=xL4qz&pd_rd_r=c3b7ef46-f4ee-485b-84c6-f3cf68a667a7&pd_rd_i=B0BVD8LZQL&th=1",
        flipfinallink, finalsellerlink] 
        } 
        var options = { 
            method: 'POST', 
            uri: 'http://127.0.0.1:6500/array', 
            body: data, 
            json: true
        }; 
    
        var sendrequest = await request(options) 
    
            .then(function (parsedBody) { 
                console.log(parsedBody);
                let result; 
                result = parsedBody['result']; 
                var propertyName = Object.keys(parsedBody.GEM)[3];
                // console.log(propertyName);
    // var propertyName = Object.keys(parsedBody.GEM)[31];
    // console.log(propertyName);
    proimage1 = parsedBody.GEM.img1;
    proimage2 = parsedBody.GEM.img3;
    proimage3 = parsedBody.GEM.img4;
    proname = parsedBody.GEM.name;
    promodel = parsedBody.GEM.model;
    probrand = parsedBody.GEM.brand; 
    prostock = parsedBody.GEM.in_stock;
    prominqty = parsedBody.GEM.minimum_quantity;
    pro_id = parsedBody.GEM.product_id;
    proorigin = parsedBody.GEM.origin;
    proprice = parsedBody.GEM.price;
    pro_pricefor = parsedBody.GEM.pricefor;
    pro_sellertype = parsedBody.GEM.sellertype;
    pro_sellervari = parsedBody.GEM.verificationstatus;
    prorating = parsedBody.GEM.rating;
    sellerlink = parsedBody.GEM.sellerslink;
    proprocessordesc = parsedBody.GEM.Processor_Number;
    prographictype = parsedBody.GEM.Graphics_Type;
    prographicdesc = parsedBody.GEM.Graphic_Card_Description;
    prooperatingsys = parsedBody.GEM.Operating_System__Factory_Pre_Loaded_;
    proramtype = parsedBody.GEM.Type_of_RAM;
    proramsize = parsedBody.GEM.RAM_Size__GB_;
    prohddsize = parsedBody.GEM.Total_HDD_Capacity__GB_; 
    prossdsize = parsedBody.GEM.Capacity_of_each_SSD__GB_;
    prodisplay = parsedBody.GEM.Display_Size__Inch_;
    prodisplayreso = parsedBody.GEM.Display_Resolution__Pixels_;
    prowarranty = parsedBody.GEM.On_Site_OEM_Warranty__Year__OEM__Authorised_channel_partner_shall_note_that_W_G_to_be_fulfilled_by_OEM_at_site_ ;
    fliptitle = parsedBody.FLIPKART.title;
    flipprobrand = parsedBody.FLIPKART.Processor_Brand;
    flipproname = parsedBody.FLIPKART.Processor_Name;
    flipprogen = parsedBody.FLIPKART.Processor_Generation;
    flipramsize = parsedBody.FLIPKART.RAM;
    flipramtype = parsedBody.FLIPKART.RAM_Type;
    flipscreensize = parsedBody.FLIPKART.Screen_Size;
    flipscreenpixel = parsedBody.FLIPKART.Screen_Resolution;
    flipssdsize = parsedBody.FLIPKART.SSD_Capacity;
    flipwarranty = parsedBody.FLIPKART.Warranty_Summary;
    flipgraphics = parsedBody.FLIPKART.Graphic_Processor;       
                }) 
            .catch(function (err) { 
                console.log(err); 
            }); 
    } 


    var sellerlinkarr = [];
    var finalsellerlink;

    const { spawn } = require('child_process');
const { validateHeaderValue } = require("http");

    async function runPythonScript() {
        const pythonProcess = spawn('python', ['app.py'], {
            detached: true,
            stdio: 'ignore',
        });
    
        // Detach the child process to let it run independently
        pythonProcess.unref();
    
        // Optional: Wait for a certain time before considering it successful
        await new Promise((resolve) => setTimeout(resolve, 1000));
    
        return Promise.resolve();
    }
    
    async function handleProductPost(req, res, index) {
        finallink = linkarr[index];
        // flipLink = fliplink[index];
        flipprice = fliparr[index];
        // flipName = flipname[index];
        flipfinallink = fliplinkarr[index];
        // console.log(flipfinallink);
        ebaylink = ebaylinkarr[index];
        ebayname = ebaytitlearr[index];
        ebayprice = ebayarr[index];

        finalsellerlink = sellerlinkarr[index];
        console.log(finalsellerlink);

        // console.log(flipfinallink);
    
        try {
            await runPythonScript();
            await arraysum();
            res.redirect("/product_details");
        } catch (error) {
            console.error(error);
            res.status(500).send('Internal Server Error');
        }
    }
   
    app.post("/product1", async function(req, res) {

        await handleProductPost(req, res, 0);

    });
    
    app.post("/product2", async function(req, res) {
        await handleProductPost(req, res, 1);

    });
    
    app.post("/product3", async function(req, res) {
        await handleProductPost(req, res, 2);
    });
    
    app.post("/product4", async function(req, res) {
        await handleProductPost(req, res, 3);

    });
    
    app.post("/product5", async function(req, res) {
        await handleProductPost(req, res, 4);

    });
    
    app.post("/product6", async function(req, res) {
        await handleProductPost(req, res, 5);
    });


app.post("/gemvisit", function(req, res){
    res.redirect(finallink);
});
app.post("/flipkartvisit", function(req, res){
    res.redirect(flipfinallink);
});
app.post("/ebayvisit", function(req, res){
    res.redirect(ebaylink);
});

app.listen(3000, function(){
    console.log("Server started at port 3000");
});


var searchingTitle = "Get the pricing and comparison details of your searched product right here!";
var cardS = [];


function isSearchingForLaptop(userInput) {
    const lowercasedInput = userInput.toLowerCase();
    const containsLaptop = lowercasedInput.includes('laptop');

    return containsLaptop;
}

var searchinputflipkart = "";
var fliparr = [];
var ebayarr = [];
var fliplinkarr = [];
var fliptitlearr = [];
var ebaylinkarr = [];
var ebaytitlearr = [];
var flipratingarr = [];
var ebayratingarr = [];
var searchInput;


app.post("/searching", async function(req, res) {
    searchInput = req.body.searchValue;
    searchinputflipkart = req.body.searchValue;
    laptoptrue = "false";
    cardS = [];
    linkarr = [];
    flagg = 1;
    fliparr = [];
    ebayarr = [];
    fliplinkarr = [];
    fliptitlearr = [];
    ebaylinkarr = [];
    ebaytitlearr = [];
    flipratingarr = [];
    ebayratingarr = [];
    searchingTitle = "Price and Details of Searched Product";

    try {
        await Promise.all([processExcelFile(filePath), flipsearch()]);

        res.redirect("/");
    } catch (error) {
        console.error('Error in /searching:', error);
        res.status(500).send('Internal Server Error');
    }
});


async function flipsearch() {
    fliparr = [];
    ebayarr = [];
    fliplinkarr = [];
    fliptitlearr = [];
    ebaylinkarr = [];
    ebaytitlearr = [];
    flipratingarr = [];
    ebayratingarr = [];
    return new Promise(async (resolve, reject) => {
        var data = {
            array: [searchinputflipkart]
        };

        var options = {
            method: 'POST',
            uri: 'http://127.0.0.1:8000/ebay',
            body: data,
            json: true
        };

        try {
            const parsee = await request(options);
            // console.log(parsee);

            if (parsee && parsee.flipkart) {
                for (var i = 5; i < (linkarr.length + 5); i++) {
                    var price = parsee.flipkart[i].price;
                    fliparr.push(price);
                    var flink = parsee.flipkart[i].link;
                    fliplinkarr.push(flink);
                    var fname = parsee.flipkart[i].title;
                    fliptitlearr.push(fname);
                    var frate = parsee.flipkart[i].rating;
                    flipratingarr.push(frate);
                }
                // console.log(parsee);
            }

            if (parsee && parsee.ebay) {
                for (var i = 5; i < (linkarr.length + 5); i++) {
                    var priceInDollars = parsee.ebay[i].price;
                    var priceInRupees = convertToRupees(priceInDollars);
                    ebayarr.push(priceInRupees);
                    var elink = parsee.ebay[i].link;
                    ebaylinkarr.push(elink);
                    var etitle = parsee.ebay[i].title;
                    ebaytitlearr.push(etitle);
                    var erate = (parsee.ebay[i].rating).substring(0,3);
                    ebayratingarr.push(erate);
                }
            }

            resolve();
        } catch (err) {
            console.error(err);
            reject(err); 
        }
    });
}




const filePath = "datascrap.xlsx";

async function processExcelFile(filePath) {
    laptoptrue = isSearchingForLaptop(searchInput);

    if (searchInput) {
        try {
            const workbook = await readExcelFile(filePath);
            const sheetName = workbook.SheetNames[0];
            const worksheet = workbook.Sheets[sheetName];

            const productData = XLSX.utils.sheet_to_json(worksheet);

            const searchKeywords = searchInput.toLowerCase().split(/\s+/);
            const matchingProducts = productData.filter((product) => {
                const productName = String(product["ProductName"]).toLowerCase();
                return searchKeywords.every(keyword => productName.includes(keyword));
            });

            if (matchingProducts.length < 6 && matchingProducts.length > 0) {
                for (var i = 0; i < matchingProducts.length; i++) {
                    cardS.push(matchingProducts[i]);
                    linkarr.push(matchingProducts[i].link);

                    var linkss = matchingProducts[i].sellerLink;
                    sellerlinkarr.push(linkss);
                };
            } else if (matchingProducts.length >= 6) {
                for (var i = 0; i <= 5; i++) {
                    cardS.push(matchingProducts[i]);
                    linkarr.push(matchingProducts[i].link);

                    var linkss = matchingProducts[i].sellerLink;
                    sellerlinkarr.push(linkss);

                };
            }
        } catch (error) {
            console.error('Error reading Excel file:', error);
        }
    }
}

async function readExcelFile(filePath) {
    try {
        const data = fs.readFileSync(filePath);
        const workbook = XLSX.read(data, { type: 'buffer' });
        return workbook;
    } catch (error) {
        throw error;
    }
}

function convertToRupees(priceInDollars) {
    const exchangeRate = 75;
    const numericPrice = parseFloat(priceInDollars.replace(/\$/g, ''));
    if (!isNaN(numericPrice)) {
        const priceInRupees = (numericPrice * exchangeRate).toFixed(2);
        return priceInRupees;
    } else {
        console.error(`Invalid price format: ${priceInDollars}`);
        return null;
    }
}


app.get("/sellers", function(req, res){
    sellers_detail();
});


async function sellers_detail() { 

    var data = { 
        array: ["https://mkp.gem.gov.in/laptop-notebook/hp-247-g8-ryzen3-athlon-3045b-win11h-8133/p-5116877-32989524800-cat/all_sellers.html"] 
    } 

    var options = { 
        method: 'POST', 
        uri: 'http://127.0.0.1:6000/selller', 
        body: data, 
        json: true
    }; 

    var sendrequest = await request(options) 

        .then(function (parseed) { 
            console.log(parseed);
            let result; 
            result = parseed['result'];
         }) 
        .catch(function (err) { 
            console.log(err); 
        }); 
} 


