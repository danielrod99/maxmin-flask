

var app = angular.module('maxmin', []);
app.controller('max-minCtrl', function ($scope,$http) {
    $scope.restricciones = [];
    $scope.maxomin = 'max';
    $scope.numRestricciones = 'select';
    $scope.todosValidos = []
    $scope.formaCanonica={
        x1:0,
        x2:0
    }
    $scope.llenarRestricciones = function () {
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
        console.log($scope.restricciones)
        $http.post('/calcular',JSON.stringify($scope.restricciones)).then((result)=>{
            console.log(result)
        })
        
    }
});

