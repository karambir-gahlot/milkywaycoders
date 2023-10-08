console.log('Main js script loaded')

function setCookie(name,value) {
    document.cookie = name + "=" + value + "; path=/";
}

$("#mysatellites").change(function() {
    console.log("Satellites selected: " + $(this).val());
    setCookie("mysatellites", $(this).val().join(","))
    location.reload()
});