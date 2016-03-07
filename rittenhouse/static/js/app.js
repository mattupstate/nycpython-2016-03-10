angular.module('rittenhouse', ['ngMaterial', 'angular-hal', 'ngWebSocket'])

  .service('$rittenhouse', function($q, $window, $websocket, halClient) {
    var self = this;
    var rootResource;
    var objectCreatedEvent = 'object-created';
    var objectMessageEvent = 'object-message';

    var eventHandlers = {};
    [objectCreatedEvent, objectMessageEvent].forEach(function(item) {
      eventHandlers[item] = [];
    });

    function registerEventHandler(event, handler) {
      var handlers = eventHandlers[event];
      if (angular.isUndefined(handlers)) {
        throw event + " is not a known event type";
      } else if (! typeof v === "function") {
        throw "handler must be a function";
      } else if (handlers.indexOf(handler) === -1) {
        handlers.push(handler);
      }
    }

    function handleMessage(message) {
      var handlers = eventHandlers[message.event];
      if (angular.isUndefined(handlers)) {
        throw message.event + " is not a known event type";
      } else {
        handlers.forEach(function(item) {
            item(message);
          });
      }
    }

    function onMessage(message) {
      var message = JSON.parse(message.data);
      if (angular.isUndefined(message.event)) {
        throw "message does not contain an event";
      } else {
        handleMessage(message);
      }
    }

    function makeWebsocketUri(href) {
      return 'ws://' + $window.location.host + href;
    }

    function initWebSocket() {
      var href = makeWebsocketUri(rootResource.$href('objects'));
      $websocket(href).onMessage(onMessage);
    }

    this.init = function() {
      return $q(function(resolve, reject) {
        halClient.$get('/')
          .then(function(res) {
            rootResource = res;
            self.getObjects()
              .then(function(objects) {
                initWebSocket();
                resolve(objects);
              });
          });
      });
    };

    this.getObjects = function() {
      return $q(function(resolve, reject) {
        rootResource.$get('objects')
          .then(function(objects) {
            objects.$get('items')
              .then(function(items) {
                resolve(items);
              });
          });
      });
    };

    this.newObject = function() {
      return rootResource.$post('objects', null, {});
    };

    this.sendObjectMessage = function(obj) {
      var event = {message: "Hello!"};
      rootResource.$post('object', {uuid:obj.uuid}, event);
    }

    this.onObjectCreated = function(handler) {
      registerEventHandler(objectCreatedEvent, handler);
    };

    this.onObjectMessage = function(handler) {
      registerEventHandler(objectMessageEvent, handler);
    }
  })

  .controller('AppCtrl', function($scope, $rittenhouse) {
    $scope.objects = [];
    $scope.events = {};
    $scope.colors = ['gray', 'green', 'yellow', 'blue', 'purple', 'red'];

    $scope.newObject = function() {
      $rittenhouse.newObject();
    }

    $scope.sendObjectMessage = function(object) {
      $rittenhouse.sendObjectMessage(object);
    }

    function addObjects(objects) {
      objects.forEach(function(item) {
        $scope.events[item.uuid] = [];
      });
      $scope.objects = $scope.objects.concat(objects);
    }

    function onObjectMessage(event) {
      var payload = event.payload;
      var obj = payload.object;
      var message = payload.message;
      $scope.events[obj.uuid].push(message);
    }

    function onObjectCreated(event) {
      addObjects([event.payload.object]);
    }

    $rittenhouse.onObjectCreated(onObjectCreated);
    $rittenhouse.onObjectMessage(onObjectMessage);

    $rittenhouse.init()
      .then(function(objects) {
        addObjects(objects);
      });
  })

  .config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
  });
