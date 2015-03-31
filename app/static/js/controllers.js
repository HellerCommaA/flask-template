angular.module('invman', [])

  .service('InventoryItems',function($http){
    
    function parseResponse(res){
      return res.data.json_list;
    }
    
    
    this.loadItems = function(){
      return $http.get('/item')
      .then(parseResponse);
    }
    
  })
  .directive('item',function(){
    
    return {
      restrict: 'A',
      replace: true,
      scope: {
        'item': '=',
        'click': '&'
      },
      templateUrl: '/static/angular/item-view.html'
      }
  })
  .controller('InvItems', function($scope,InventoryItems) {
    $scope.itemDetail = function(item) {
      alert('in detail for ' + item)
    };

    InventoryItems.loadItems().then(function(items){
      $scope.items = items; 
    });
    
  });