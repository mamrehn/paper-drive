var app = angular.module('app', ['ngAnimate', 'ui.grid', 'ui.grid.autoResize', 'ui.grid.edit']);

app.controller('MainCtrl', ['$scope', '$http', 'uiGridConstants', function ($scope, $http, uiGridConstants) {

    // http://stackoverflow.com/questions/18310007/add-html-link-in-anyone-of-ng-grid
    //var linkCellTemplate = '<div class="ngCellText" ng-class="col.colIndex()">' +
    //                   '  <a href="file:///{{grid.getCellValue(row, col["full_path"])}}">{{grid.getCellValue(row, col)}}</a>' +
    //                   '</div>';
    //var linkCellTemplate2 = '<div class="ngCellText" ng-class="col.colIndex()">' +
    //                   "  {{grid.getCellValue(row, col)}}" + '</div>';

    // http://ui-grid.info/docs/#/tutorial/305_appScope
    var titleCellTemplate = '<div class="ngCellText ui-grid-cell-contents" ng-class="col.colIndex()">' +
        '<a ng-click="grid.appScope.myNewModel.goToFile(row.entity)">{{grid.getCellValue(row, col)}}</a>' +
        '</div>';

    // var linkCellTemplate = '<a href="file:///{{grid.getCellValue(row, col)}}"><button id="editBtn" type="button" class="btn-small" >link</button></a>'
    // grid.appScope.edit(row.entity)

    // http://stackoverflow.com/questions/23646395/rendering-a-star-rating-system-using-angularjs
    var ratingCellTemplate = '<div class="ngCellText" ng-class="col.colIndex()">' +
        '<div star-rating rating-value="grid.getCellValue(row, col)" max="4" ></div>' +
        '</div>';

    // Access outside scope functions from row template
    $scope.myNewModel = {
        goToFile: function(row) {
            //alert(JSON.stringify(row));
            //console.log(row);
            window.open('/data/papers/' + row['path']);
        }
    };

//    // http://stackoverflow.com/questions/16824853/way-to-ng-repeat-defined-number-of-times-instead-of-repeating-over-array
//    $scope.getNumber = function(num) {
//        return new Array(num);
//    }

    $scope.gridOptions = {
        enableHorizontalScrollbar: uiGridConstants.scrollbars.NEVER,
        enableFiltering: true,
        showFooter: true,
        //showGroupPanel: true,
        columnDefs: [
            {
              field: 'rating',
              enableCellEdit: false,
              aggregationType: uiGridConstants.aggregationTypes.avg,
              aggregationHideLabel: true,
              width: 68,
              cellTemplate: ratingCellTemplate,
              filters: [
                    {
                        condition: uiGridConstants.filter.GREATER_THAN_OR_EQUAL,
                        placeholder: 'min'
                    },
                    {
                        condition: uiGridConstants.filter.LESS_THAN_OR_EQUAL,
                        placeholder: 'max'
                    }
              ]
            },
            {
                field: 'title',
                enableCellEdit: false,
                aggregationType: uiGridConstants.aggregationTypes.count,
                cellTemplate: titleCellTemplate,
                filters: [
                    {
                    condition: uiGridConstants.filter.CONTAINS,
                    placeholder: 'contains'
                    },
                    {
                    condition: uiGridConstants.filter.STARTS_WITH,
                    placeholder: 'starts with'
                    }
                ]
            },
            // pre-populated search field
            {
                field: 'year',
                aggregationType: uiGridConstants.aggregationTypes.min,
                width: 75,
                filters: [
                    {
                        condition: uiGridConstants.filter.GREATER_THAN_OR_EQUAL,
                        placeholder: 'min'
                    },
                    {
                        condition: uiGridConstants.filter.LESS_THAN_OR_EQUAL,
                        placeholder: 'max'
                    }
                ]
            },
            // no filter input
            {
                field: 'citations',
                aggregationType: uiGridConstants.aggregationTypes.avg,
                aggregationHideLabel: true,
                width: 75,
                filters: [
                    {
                        condition: uiGridConstants.filter.GREATER_THAN_OR_EQUAL,
                        placeholder: 'min'
                    },
                    {
                        condition: uiGridConstants.filter.LESS_THAN_OR_EQUAL,
                        placeholder: 'max'
                    }
                ]
            },
            {
                field: 'publisher',
                //aggregationType: uiGridConstants.aggregationTypes.count,
                width: 100,
                filter: {
                    condition: uiGridConstants.filter.CONTAINS,
                    placeholder: 'contains'
                }
            },
            {
                field: 'author',
                //aggregationType: uiGridConstants.aggregationTypes.count,
                width: 100,
                filter: {
                    condition: uiGridConstants.filter.CONTAINS,
                    placeholder: 'contains'
                }
            }//,
//            {
//                field: 'full_path',
//                displayName: 'Link',
//                //aggregationType: uiGridConstants.aggregationTypes.count,
//                //aggregationHideLabel: true,
//                enableCellEdit: false,
//                //visible: false,
//                cellTemplate: linkCellTemplate,
//                //filter: {
//                //    condition: uiGridConstants.filter.STARTS_WITH,
//                //    placeholder: 'starts with'
//                //},
//                width: 70
//            }
        ]
    };

    $http.get('/data/papers.json')
        .success(function(data) {
            $scope.gridOptions.data = data;
        });

    //console.log(window.innerHeight);
    //angular.element(document.getElementsByClassName('myGrid')[0]).css('height', window.innerHeight * 0.8 + 'px');
    //angular.element(document.getElementsByClassName('grid')[0]).css('width', newWidth + 'px');

}]);


app.directive('starRating', function () {
    return {
        restrict: 'A',
        template: '<ul class="rating">' +
            '<li ng-repeat="star in stars" ng-class="star">' +
            '\u2605' +
            '</li>' +
            '</ul>',
        scope: {
            ratingValue: '=',
            max: '='
        },
        link: function (scope, elem, attrs) {
            scope.stars = [];
            for (var i = 0; i < scope.max; i++) {
                scope.stars.push({
                    filled: i < scope.ratingValue
                });
            }
        }
    };
});