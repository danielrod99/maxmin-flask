

var app = angular.module('maxmin', []);
app.controller('max-minCtrl', function ($scope,$http) {
    $scope.restricciones = [];
    $scope.maxomin = 'Maximizar';
    $scope.numRestricciones = 'select';
    $scope.todosValidos = []
    $scope.formaCanonica={
        x1:0,
        x2:0
    }
    $scope.showGraph=false;
    $scope.llenarRestricciones = function () {
        $scope.showGraph=false;
        $scope.restricciones = [];
        var numero=parseInt($scope.numRestricciones);
        for (let i = 0; i < numero; i++) {
            $scope.restricciones.push({
                x1: 0,
                x2: 0,
                igualador: '<=',
                resultado: 0,
            });
        }
    }    
    $scope.calcular=function(){
        $scope.showGraph=false;
        console.log($scope.restricciones)
        var fullBody={
            "maxomin": $scope.maxomin,
            "canonica": $scope.formaCanonica,
            "restricciones": $scope.restricciones
        }
        $http.post('/calcular',JSON.stringify(fullBody)).then((result)=>{
            console.log(result)
            if(typeof(result.data)=='string'){
                alert('Hay una indeterminacion');
            }else{
                $scope.resFunObj=result.data.resFunObj;
                $scope.puntos=result.data.puntos;
                $scope.showGraph=true;
                document.getElementById('img').innerHTML=`<img src="../static/grafica.png" alt="Grafica">`
                document.querySelector('.funcObj').innerHTML=`<p>Resultado:</p><p>x1 = ${$scope.resFunObj.x1}</p><p>x2 = ${$scope.resFunObj.x2}</p><p>Resultado Funcion Objetivo = ${$scope.resFunObj.resultado}</p>`
                var puntos='<p>Puntos:</p>';
                for(let i=0;i<$scope.puntos.length;i++){
                    puntos+=`<p>[ ${$scope.puntos[i][0]} , ${$scope.puntos[i][0]} ]</p>`;
                }
                document.querySelector('.puntos').innerHTML=puntos;
            }
        })
        
    }
});

