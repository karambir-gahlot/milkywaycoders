console.log('Main js script loaded')

function setCookie(name,value) {
    document.cookie = name + "=" + value + "; path=/";
}

function selectSatellites(satellites) {
    console.log("Satellites selected: " + satellites);
    setCookie("mysatellites", satellites.join(","))
    location.reload()
}

$("#mysatellites").change(function() {
    selectSatellites($(this).val());
});