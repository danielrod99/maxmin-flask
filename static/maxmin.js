

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
        var fullBody={
            "maxomin": $scope.maxomin,
            "canonica": $scope.formaCanonica,
            "restricciones": $scope.restricciones
        }
        $http.post('/calcular',JSON.stringify(fullBody)).then((result)=>{
            console.log(result)
        })
        
    }
});

