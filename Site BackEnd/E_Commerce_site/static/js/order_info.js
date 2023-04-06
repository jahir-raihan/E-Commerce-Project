let dc = document;


// Selected payment method


let payment_method = 'cod';

let cod = dc.getElementById('cod')
let bksh = dc.getElementById('bkash')
let sslcom = dc.getElementById('sslcom')
let choices = dc.querySelectorAll('.choice-card')
choices.forEach ( (choice) => {
    choice.addEventListener( 'click', function(){

        if (choice.id == 'cod'){
            payment_method = 'cod';
            cod.classList.add('choice-selected')
            bksh.classList.remove('choice-selected')
            sslcom.classList.remove('choice-selected')

        }
        else if (choice.id == 'bkash'){
            payment_method = 'bkash';
            bksh.classList.add('choice-selected')
            cod.classList.remove('choice-selected')
            sslcom.classList.remove('choice-selected')

        }
        else if (choice.id == 'sslcom'){
            payment_method = 'sslcom';
            sslcom.classList.add('choice-selected')
            bksh.classList.remove('choice-selected')
            cod.classList.remove('choice-selected')

        }
    })
})

// End Selected payment method



// Selected Saved address , if saved

let saved_address_selected = null

let addresses = dc.querySelectorAll('.address')
let address_info = dc.querySelectorAll('.address-info')

addresses.forEach( (address) => {
    address.addEventListener('click', function(){
        saved_address_selected = address.id;

        address_info.forEach((ad_info) => {

            ad_info.classList.remove('address-selected')
        });
        address.children[0].classList.add('address-selected')
    })
})

// End selected saved address