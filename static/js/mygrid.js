var app = angular.module('app', ['ngAnimate', 'ui.grid', 'ui.grid.autoResize', 'ui.grid.edit']);

app.controller('MainCtrl', ['$scope', '$http', 'uiGridConstants', function ($scope, $http, uiGridConstants) {

    // http://stackoverflow.com/questions/18310007/add-html-link-in-anyone-of-ng-grid
    var linkCellTemplate = '<div class="ngCellText" ng-class="col.colIndex()">' +
                       '  <a href="file:///{{row.getProperty(col.field)}}">Visible text</a>' +
                       '</div>';
    var linkCellTemplate2 = '<div class="ngCellText" ng-class="col.colIndex()">' +
                       "  {{row.getProperty(col.field)}}" + '</div>';

    $scope.gridOptions = {
        enableFiltering: true,
        showFooter: true,
        //showGroupPanel: true,
        columnDefs: [
            // default
            {
                field: 'title',
                enableCellEdit: false,
                aggregationType: uiGridConstants.aggregationTypes.count,
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
                filters: [
                    {
                        condition: uiGridConstants.filter.GREATER_THAN_OR_EQUAL,
                        placeholder: 'min'
                    },
                    {
                        condition: uiGridConstants.filter.LESS_THAN_OR_EQUAL,
                        placeholder: 'max'
                    }
                ],
                width: 150
            },
            // no filter input
            {
                field: 'citations',
                aggregationType: uiGridConstants.aggregationTypes.avg,
                aggregationHideLabel: true,
                width: 150,
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
                width: 150,
                filter: {
                    condition: uiGridConstants.filter.CONTAINS,
                    placeholder: 'contains'
                }
            },
            {
                field: 'path',
                displayName: 'Link',
                //aggregationType: uiGridConstants.aggregationTypes.count,
                //aggregationHideLabel: true,
                enableCellEdit: false,
                cellTemplate: linkCellTemplate,
                //filter: {
                //    condition: uiGridConstants.filter.STARTS_WITH,
                //    placeholder: 'starts with'
                //},
                width: 100
            }//,
            // custom condition function
            //{ field: 'type' }
            ,{
                field: 'full_path',
                displayName: 'Link',
                //aggregationType: uiGridConstants.aggregationTypes.count,
                //aggregationHideLabel: true,
                enableCellEdit: false,
                cellTemplate: linkCellTemplate2,
                //filter: {
                //    condition: uiGridConstants.filter.STARTS_WITH,
                //    placeholder: 'starts with'
                //},
                width: 100
            }
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