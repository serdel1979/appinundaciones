
const initialLng = -57.956;
const initialLat = -34.9187;

export class MapClass {

    constructor({selector, addSearch, latitude, longitude, marker}){
        this.initializeMap(selector, latitude, longitude, marker);

        if(addSearch){
            this.addSearchControl()
        }
        this.map.addEventListener('click', e => {
            this.addMarker(e.latlng)
        });
    }

    initializeMap(selector, latitude, longitude, marker) {
        if (!latitude) {
            latitude = initialLat;
            longitude = initialLng; 
        }
        this.map = L.map(selector).setView([latitude, longitude], 13);
        L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}',{
        maxZoom: 20,
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1,
        accessToken: 'pk.eyJ1IjoiZnJhbjEyNCIsImEiOiJja3Vvcm9xODcwYnQ0MnZwZ2xycmJlNmM4In0.fLYzh2yA4-jSF1ufvVi_mQ'
        }).addTo(this.map);
        if (marker.latitude) {
            this.marker = L.marker([marker.latitude,marker.longitude]).addTo(this.map);
        }
    }

    addMarker({lat,lng}) {
        if (this.marker) {
            this.marker.remove();
        }
        this.marker = L.marker([lat,lng]).addTo(this.map);
    }
      
    addSearchControl() {
        L.control.scale().addTo(this.map);
        let searchControl = new L.esri.Controls.Geosearch().addTo(this.map);

        let results = new L.LayerGroup().addTo(this.map);

        searchControl.on('results', data => {
            results.clearLayers();

            if (data.results.length > 0 ){
                this.addMarker(data.results[0].latlng)
            }
        });
    };

};