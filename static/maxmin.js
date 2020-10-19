

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
    $scope.nuevo=false;
    $scope.showGraph=false;
    $scope.otro=false;
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
        if($scope.revisarValores()=='error'){
            alert('Algun valor en las restricciones no es un numero');
            return
        }
        if(isNaN($scope.formaCanonica.x1)==true||isNaN($scope.formaCanonica.x2)==true){
            alert('Algun valor de la funcion Objetivo no es un numero');
            return
        }
        $scope.showGraph=false;
        console.log($scope.restricciones)
        $scope.nuevo=true;
        $scope.otro=true;
        var fullBody={
            "maxomin": $scope.maxomin,
            "canonica": $scope.formaCanonica,
            "restricciones": $scope.restricciones
        }
       // $scope.$apply();
        $http.post('/calcular',JSON.stringify(fullBody)).then((result)=>{
            console.log(result)
            if(typeof(result.data)=='string'){
                alert('Hay una indeterminacion');
                window.location.reload();
            }else{
                $scope.resFunObj=result.data.resFunObj;
                $scope.puntos=result.data.puntos;
                $scope.showGraph=true;
                $scope.otro=false;
                setTimeout(()=>{
                    document.getElementById('img').innerHTML=`<img ng-show="showGraph" src="../static/grafica.png" alt="Grafica">`
                },1000)
                document.querySelector('.funcObj').innerHTML=`<p>Resultado:</p><p>x1 = ${$scope.resFunObj.x1}</p><p>x2 = ${$scope.resFunObj.x2}</p><p>Resultado Funcion Objetivo = ${$scope.resFunObj.resultado}</p>`
                var puntos='<p>Puntos:</p>';
                for(let i=0;i<$scope.puntos.length;i++){
                    puntos+=`<p>[ ${$scope.puntos[i][0]} , ${$scope.puntos[i][1]} ]</p>`;
                }
                document.querySelector('.puntos').innerHTML=puntos;
            }
        })
        
    }
    $scope.ajustarEstilos=function(){
        var divImg= document.getElementById('img');
        var dataDiv= document.querySelector('.puntosResp');
        var resultDiv=document.querySelector('.funcObj');
        var puntos= document.querySelector('.puntos');
        divImg.style.float='left';
        dataDiv.style.float='left';
        resultDiv.style.float='left';
        puntos.style.float='left';

        divImg.style.width='50%';
        dataDiv.style.width='50%';
        resultDiv.style.width='50%';
        puntos.style.width='50%';
    }
    $scope.reloading=function(){
        window.location.reload();
    }
    $scope.revisarValores=function(){
        var hayError=false;
        $scope.restricciones.forEach((item,index)=>{
            if(isNaN(item.x1)==true){
                hayError=true;
                return 'error'
            }
            if(isNaN(item.x2)==true){
                hayError=true;
                return 'error'
            }
            if(isNaN(item.resultado)==true){
                hayError=true;
                return 'error'
            }

        })
        if(hayError){
            return 'error'
        }else{
            return 'ok'
        }
    }
});

