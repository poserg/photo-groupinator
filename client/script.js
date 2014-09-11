//(function() {

    var proxiedSync = Backbone.sync;
/*
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
  $.ajaxPrefilter( function( options, originalOptions, jqXHR ) {
    options.crossDomain ={
        crossDomain: true
    };/*
    options.xhrFields = {
        withCredentials: true
    };*/
    options.url = 'http://localhost:8080' + options.url;
  });

  
  var Image = Backbone.Model.extend({
    defaults: {
      id: "",
      name: "",
      path: ""
    },
    url: function() {
      return "http://localhost:8080/photo/" + this.id;
    }
    //urlRoot: "/photo"
  });

  var ImageView = Backbone.View.extend({
    initialize: function() {

    },
    
    template: _.template($('#image-template').html()),

    render: function() {
      this.$el.html(this.template(this.model.toJSON()));

      return this;
    }
  });

  var ImageCollection = Backbone.Collection.extend({

    url: "/photo",
    
    model: Image
  });

  var ImageCollectionView = Backbone.View.extend({
    //tagName: 'ol'

  /*   initialize: function () {
        $.ajaxPrefilter( function( options, originalOptions, jqXHR ) {
        // Your server goes below
        options.url = 'http://localhost:5000' + options.url;
        //options.url = 'http://cross-domain.nodejitsu.com' + options.url;
      });
     }*/
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

  var imageCollection = new ImageCollection();
  imageCollection.fetch();
  var imageCollectionView = new ImageCollectionView({
    collection: imageCollection
  });
  $('body').append(imageCollectionView.render().el);
//})();
