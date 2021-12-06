// import { MapClass as Map } from '../../MapSingleMarkerClass.js';
 import {MapClass as Map} from './MapMarkerClass.js'
// import { Map } from './MapSingleMarker.js'

const submitHandler = (event, map) => {

    if (!map.marker) {
        event.preventDefault();
        alert('Debes seleccionar una ubicacion en el mapa.');
    }
    else {
        const latlng = map.marker.getLatLng()
        document.getElementById('lat').setAttribute('value', latlng.lat);
        document.getElementById('lng').setAttribute('value', latlng.lng);
    }
}

window.onload = () => {
    let lat = (document.getElementById("lat").value ? document.getElementById("lat").value : null);  
    let lng = (document.getElementById("lng").value ? document.getElementById("lng").value : null);  

    const map = new Map({
        selector: 'map',
        addSearch: true,
        latitude: lat,
        longitude: lng,
        marker: {
            latitude: lat, 
            longitude:lng,
        }
    });


    const form = document.getElementById('complaint-form');

    form.addEventListener('submit', (event) => submitHandler(event, map));

}
