document.getElementById("search-icon").addEventListener("click", function () {
    document.getElementById("search-container").style.display = "flex";
});

function closeSearch() {
    document.getElementById("search-container").style.display = "none";
}


//
// function postQuery(data) {
//     fetch('http://127.0.0.1:8000/api/api_order_create/',
//         {
//             options: 'GET',
//         }).then(response => response.json())
//         .then(data => console.log(data)).catch(error => {
//         console.log(`The fucking error: ${error}`)
//     })
// }
//
// fetch('http://127.0.0.1:8000/api/api_order_create/',
//     {options: 'GET'})
//     .then(response => response.json())
//     console.log(.then(response => response.json())



