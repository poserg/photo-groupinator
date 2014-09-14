//(function() {
/*
    var proxiedSync = Backbone.sync;
    Backbone.sync = function(method, model, options) {
      options || (options = {});

      if (!options.crossDomain) {
        options.crossDomain = true;
      }

      if (!options.xhrFields) {
        options.xhrFields = {withCredentials:true};
      }

      return proxiedSync(method, model, options);
    };
  })();
*/
  var vent = {};
  _.extend(vent, Backbone.Events);

  /*
  $.ajaxSetup({
    headers: { 'X-Requested-With' : 'XMLHttpRequest' }
  });
*/
var serverPath = 'http://localhost:8080';

  $.ajaxPrefilter( function( options, originalOptions, jqXHR ) {
    options.crossDomain ={
        crossDomain: true
    };/*
    options.xhrFields = {
        withCredentials: true
    };*/
    options.url = serverPath + options.url;
  });

var Group = Backbone.Model.extend({
  url: function() {
    return "/group/" + this.id;
  }
});

var Operation = Backbone.Model.extend({
  url: function() {
    return "/operation";
  }
});

  var Image = Backbone.Model.extend({
    defaults: {
      id: "",
      name: "",
      path: ""
    },
    url: function() {
      return "/photo/" + this.id;
    },

    initialize: function() {
      this.os
      this.path = serverPath + '/static/thumbs/' + this.name;
    }
    //urlRoot: "/photo"
  });

  var ImageView = Backbone.View.extend({
    tagName: 'li',
    
    initialize: function() {

    },
    
    template: _.template($('#image-template').html()),

    render: function() {
      console.log("Start ImageView.render()");
      this.$el.html(this.template(this.model.toJSON()));

      return this;
    }
  });

var ThumbView = Backbone.View.extend({
  template: _.template($('#thumb-template').html()),

  render: function() {
    this.$el.html(this.template(this.model.toJSON()));

    return this;
  }
});

  var ImageCollection = Backbone.Collection.extend({
    model: Image,
    url: "/photo",

    initialize: function() {
      this.on('add', this.addOne, this);
    },

    addOne: function(img) {
      img.set('path', serverPath + '/static/thumbs/' + img.get('name'));
    },

    fetchSuccess: function(collection, response) {
      console.log('Collection fetch success', response);
      console.log('Collection models: ', this.collection);
    },

    fetchError: function (collection, response) {
        throw new Error("Books fetch error");
    },

    parse: function(response) {
      return response.photos;
    }
  });

  var ImageCollectionView = Backbone.View.extend({
    //tagName: 'ol',

  /*   initialize: function () {
        $.ajaxPrefilter( function( options, originalOptions, jqXHR ) {
        // Your server goes below
        options.url = 'http://localhost:5000' + options.url;
        //options.url = 'http://cross-domain.nodejitsu.com' + options.url;
      });
     }*/

    initialize: function() {
      console.log("ImageCollectionView.initialize");
      // console.log(this.collection.length);
      this.collection.bind("reset", this.render);
      //this.collection.fetch();
    },
    
    render: function() {
      console.log("Start ImageCollectionView.render");
      // console.log(this.collection.lenght);
      this.collection.each(function(img) {
        var thumbView = new ThumbView({ model: img });
        this.$el.append(thumbView.render().el);
      }, this);

      return this;
    }
  });

  var imageCollection = new ImageCollection;

  var AddNewGroupView = Backbone.View.extend({
    el: '#add-new-group',
    events: {
      'submit': 'submit'
    },

    submit: function(e) {
      e.preventDefaults();

      var group = new Group({
      });
    }
  });

var imageCollection = new ImageCollection;
imageCollection.fetch({
  success: function() {
    var imageCollectionView = new ImageCollectionView({
      collection: imageCollection
    });
    $('#app').append(imageCollectionView.render().el);
  }
});

var Router = Backbone.Router.extend({
  routes: {
    'g:group(/i:img)': 'show'
  },

  show: function(group, img) {
    console.log('group = ' + group + ', img = ' + img + '.');
  }
});

var router = new Router;
Backbone.history.start();
//})();
