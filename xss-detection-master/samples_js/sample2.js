function search() {
    const query = document.getElementById('search').value
    window.location.href = window.location.href.split('?')[0] + "?q=" + query
}
document.getElementById('searchbtn').addEventListener('click', search)

const query = (new URLSearchParams(location.search)).get('q');
if (query) {
    document.getElementById("reflect").innerHTML = `Search results for ${query}`
}

