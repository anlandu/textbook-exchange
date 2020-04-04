let btitle = "";
let bauthor = "";
let bisbn = "";

function sellUpdateSearch(search){
    if(search.length >= 2){
        //console.log(search);

        var xmlhttp = new XMLHttpRequest();

        xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == XMLHttpRequest.DONE) {   // XMLHttpRequest.DONE == 4
                if (xmlhttp.status == 200) {
                    $('#sell_results_dropdown').show(); //open the dropdown menu
                    var searchResults = JSON.parse(xmlhttp.responseText);
                    //console.log(searchResults);

                    //calculate number of dropdown items per section
                    let book_display_count = Math.round(4.0 * (parseFloat(searchResults['books'].length) / (searchResults['books'].length + searchResults['courses'].length)));

                    //update dropdown with availible results
                    if(searchResults['books'].length > 0){
                        document.getElementById("sell_results_books").style.display = 'inline'; //show header
                        var isbnList = document.getElementById("sell_book_results");
                        isbnList.innerHTML = ''; //remove old list elements
                        for(var i = 0; i < searchResults['books'].length; i++){ //add new elements
                            let book = JSON.parse(searchResults['books'][i]);

                            let entry = document.createElement('div');
                            entry.classList = "py-2 search-entry";
                            entry.style.height = '65px';

                            let row = document.createElement('div');
                            row.classList = 'row mx-0';

                            let dataCol = document.createElement('div');
                            dataCol.classList = "col-12";

                            let oneLineStyle = "white-space: nowrap; overflow: hidden; text-overflow: ellipsis;";

                            let title = document.createElement("p");
                            title.innerHTML = "<b>" + book['title']  + "</b>";
                            title.classList = 'my-0';
                            title.style = oneLineStyle;

                            let author = document.createElement("p");
                            author.innerHTML = book['author'].substring(1, book['author'].length - 2).replace(/'/g,"");
                            author.classList = 'my-0';
                            author.style = oneLineStyle;

                            dataCol.appendChild(title);
                            dataCol.appendChild(author);

                            row.appendChild(dataCol);

                            entry.appendChild(row);

                            entry.addEventListener("click", function() {
                                document.getElementById("selected-book").innerHTML = entry.innerHTML;
                                hideSearchAutocomplete();
                                btitle = book['title'];
                                bauthor = book['author'].substring(1, book['author'].length - 2).replace(/'/g,"");
                                bisbn = book['isbn13'];
                            });

                            isbnList.appendChild(entry);
                            if (i >= book_display_count) break; // only show 5 results
                        }
                    }
                    else {
                        document.getElementById("sell_results_books").style.display = 'none'; //hide section
                    }

                    if(searchResults['courses'].length > 0 || searchResults['books'].length > 0){
                        document.getElementById("sell_noresults").style.display = 'none'; //hide no results message
                    }
                    else{
                        document.getElementById("sell_noresults").style.display = 'inline'; //show no results message
                    }
                }
                else {
                    console.error("Search autocomplete not availible");
                    $('#sell_results_dropdown').hide();
                }
            }
        };

        xmlhttp.open("GET", auto_url + "?search="+search, true);
        xmlhttp.send();
    }
    else{
        $('#sell_results_dropdown').hide();
    }
};

function hideSearchAutocomplete() {
    $('#sell_results_dropdown').hide();
}

$(document).on("click touchstart", function(e) {
    var t = $(e.target).closest('#sell_results_dropdown');
    var exceptDiv = $('#sell_results_dropdown');
    var s = $(e.target).closest('#sell_search_text');
    var searchDiv = $('#sell_search_text');
    if (!exceptDiv.is(t) && !searchDiv.is(s)) hideSearchAutocomplete();
    else if (searchDiv.is(s)) sellUpdateSearch(searchDiv.val());
});

function passBookSelection() {
    document.getElementById(book_title_id).value = btitle;
    document.getElementById(book_author_id).value = bauthor;
    document.getElementById(book_isbn_id).value = bisbn;
    clearSelection();
}

function clearSelection() {
    $('#sell_results_dropdown').hide();
    document.getElementById("selected-book").innerHTML = document.createElement("p").innerHTML = "No book selected";
    document.getElementById('sell_search_text').value = "";
    btitle = "";
    bauthor = "";
    bisbn = ""
}