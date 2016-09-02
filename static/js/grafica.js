function visualizadatos(datos){
        $('#container').highcharts({
            chart: { type: 'bar' },
            title: { text: 'Visitas de los generos' },
            xAxis: { categories: datos[0] },
            yAxis: {
                title:{
                    text:'Visitas'
                }
            },
            series: [{
                data: datos[1],
                name:'numero de visitas',
            }],
        });
};
