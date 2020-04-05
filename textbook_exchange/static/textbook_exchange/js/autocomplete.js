function updateSearch(search){
    if(search.length >= 2){
        //console.log(search);

        var xmlhttp = new XMLHttpRequest();

        xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == XMLHttpRequest.DONE) {   // XMLHttpRequest.DONE == 4
                if (xmlhttp.status == 200) {
                    $('#results_dropdown').show(); //open the dropdown menu
                    var searchResults = JSON.parse(xmlhttp.responseText);
                    //console.log(searchResults);

                    //calculate number of dropdown items per section
                    let book_display_count = Math.round(4.0 * (parseFloat(searchResults['books'].length) / (searchResults['books'].length + searchResults['courses'].length)));
                    let course_display_count = Math.round(4.0 * (parseFloat(searchResults['courses'].length) / (searchResults['books'].length + searchResults['courses'].length)));

                    //update dropdown with availible results
                    if(searchResults['books'].length > 0){
                        document.getElementById("results_books").style.display = 'inline'; //show header
                        var isbnList = document.getElementById("book_results");
                        isbnList.innerHTML = ''; //remove old list elements
                        for(var i = 0; i < searchResults['books'].length; i++){ //add new elements
                            let book = JSON.parse(searchResults['books'][i]);

                            var entry = document.createElement('div');
                            entry.classList = "py-2 search-entry";
                            entry.style.height = '65px';

                            let row = document.createElement('div');
                            row.classList = 'row mx-0';

                            let pictureCol = document.createElement('div');
                            pictureCol.classList = "col-1 my-0 text-center align-self-center d-none d-lg-block px-0";

                            let picture = document.createElement('img');
                            if (book['cover_photo_url'] != '') {
                                try {
                                    //create valid json from the array
                                    jsonURL = book['cover_photo_url'];
                                    jsonURL = jsonURL.substring(0, jsonURL.indexOf(",")) + "}";
                                    jsonURL = jsonURL.replace(/'/g, "\"");
                                    picture.src = JSON.parse(jsonURL)["smallThumbnail"];
                                } catch (e) {
                                    picture.src = book['cover_photo_url'];
                                }
                            } else {
                                picture.src = 'https://isbndb.com/modules/isbndb/img/default-book-cover.jpg';
                            }
                            picture.classList = 'img-thumbnail mx-auto';
                            picture.style.maxHeight = '50px';

                            let dataCol = document.createElement('div');
                            dataCol.classList = "col-11";

                            let oneLineStyle = "white-space: nowrap; overflow: hidden; text-overflow: ellipsis;";

                            let title = document.createElement("p");
                            title.innerHTML = "<b>" + book['title']  + "</b>";
                            title.classList = 'my-0';
                            title.style = oneLineStyle;

                            let author = document.createElement("p");
                            author.innerHTML = book['author'].substring(1, book['author'].length - 2).replace(/'/g,"");
                            author.classList = 'my-0';
                            author.style = oneLineStyle;

                            let isbnP = document.createElement('p');
                            isbnP.classList = "text-muted my-0";
                            isbnP.innerHTML = "ISBN: " + book['bookstore_isbn'];

                            pictureCol.appendChild(picture);
                            dataCol.appendChild(title);
                            dataCol.appendChild(author);
                            //dataCol.appendChild(isbnP);

                            row.appendChild(pictureCol);
                            row.appendChild(dataCol);

                            entry.appendChild(row);

                            entry.addEventListener("click", function() {
                                window.location.href = '/buy/' + book['isbn13'] + "/" + book['title'].replace(/\W/g, "");
                            });

                            isbnList.appendChild(entry);
                            if (i >= book_display_count) break; // only show 5 results
                        }
                    }
                    else {
                        document.getElementById("results_books").style.display = 'none'; //hide section
                    }

                    if(searchResults['courses'].length > 0){
                        document.getElementById("results_courses").style.display = 'inline'; //show header
                        var isbnList = document.getElementById("course_results");

                        isbnList.innerHTML = ''; //remove old list elements

                        for(var i = 0; i < searchResults['courses'].length; i++){ //add new elements
                            var entry = document.createElement('div');

                            entry.classList = "py-2 search-entry";
                            entry.style.height = '65px';

                            let row = document.createElement('div');
                            row.classList = 'row mx-0';

                            let pictureCol = document.createElement('div');
                            pictureCol.classList = "col-1 my-auto mx-auto d-none d-lg-block";

                            let dataCol = document.createElement('div');
                            dataCol.classList = "col-11";

                            let oneLineStyle = "white-space: nowrap; overflow: hidden; text-overflow: ellipsis;";

                            var class_info_p = document.createElement('p');
                            class_info_p.innerHTML = "<b>" + JSON.parse(searchResults['courses'][i])['department'] + " " + JSON.parse(searchResults['courses'][i])['course_code'] + "</b>";
                            class_info_p.classList = 'my-0';
                            class_info_p.style = oneLineStyle;

                            var professor_p = document.createElement('p');
                            professor_p.innerHTML = "Section " + JSON.parse(searchResults['courses'][i])['section_number'] + " - " + JSON.parse(searchResults['courses'][i])['professor'];
                            professor_p.classList = 'my-0';
                            professor_p.style = oneLineStyle;

                            dataCol.appendChild(class_info_p);
                            dataCol.appendChild(professor_p);

                            row.appendChild(pictureCol);
                            row.appendChild(dataCol);

                            entry.appendChild(row);

                            isbnList.appendChild(entry);
                            if (i >= course_display_count) break; // only show 5 results
                        }
                    }
                    else{
                        document.getElementById("results_courses").style.display = 'none'; //hide header
                    }

                    if(searchResults['courses'].length > 0 || searchResults['books'].length > 0){
                        document.getElementById("noresults").style.display = 'none'; //hide no results message
                    }
                    else{
                        document.getElementById("noresults").style.display = 'inline'; //show no results message
                    }
                }
                else {
                    console.error("Search autocomplete not availible");
                    $('#results_dropdown').hide();
                }
            }
        };

        xmlhttp.open("GET", auto_url + "?search="+search, true);
        xmlhttp.send();
    }
    else{
        $('#results_dropdown').hide();
    }
};

function hideAutocomplete() {
    $('#results_dropdown').hide();
}

$(document).on("click touchstart", function(e) {
    var t = $(e.target).closest('#results_dropdown');
    var exceptDiv = $('#results_dropdown');
    var s = $(e.target).closest('#search_text');
    var searchDiv = $('#search_text');
    if (!exceptDiv.is(t) && !searchDiv.is(s)) hideAutocomplete();
    else if (searchDiv.is(s)) updateSearch(searchDiv.val());
});