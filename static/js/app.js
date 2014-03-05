'use strict';

var app = angular.module('ipma', ['ngRoute', 'chieffancypants.loadingBar']);

app.config(function ($routeProvider) {
    $routeProvider.when("/", {
        controller: "mainCtrl",
        templateUrl: "tpl/table.html",
        resolve: {
            getProfiles: function ($q, $http) {
                var deferred = $q.defer();
                var url = BASE_URL+"/retrieveData";
                $http.get(url).then(function(data){
                    deferred.resolve(data);
                });
                return deferred.promise;
            }
        }
    });
    $routeProvider.otherwise({ redirectTo: "/" });
});

app.controller('mainCtrl', function ($scope, $route) {
    //All data from routes (norms, profiles and steels)
    $scope.data = $route.current.locals.getProfiles.data;
});