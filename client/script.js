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
//var serverPath = 'http://192.168.1.33:8080';
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
    defaults: {
        id: "",
        name: "",
        create_date: ""
    }
});

var GroupView = Backbone.View.extend({
    template: _.template($('#group-template').html()),
    
    render: function() {
        this.$el.html(this.template(this.model.toJSON()));

        return this;
    }
});

var GroupCollection = Backbone.Collection.extend({
   model: Group, 
   url: "/groups"
});

var GroupCollectionView = Backbone.View.extend({
   el: '#group'
});

var Operation = Backbone.Model.extend({
  url: function() {
    return "/operations";
  }
});

  var Image = Backbone.Model.extend({
    defaults: {
      id: "",
      name: "",
      path: "",
      create_date: "",
      img_width: "",
      img_height: ""
    },

    initialize: function() {
      // this.os
      this.path = '/static/thumbs/' + this.name;

    }
  });

var MainImage = Image.extend({
  initialize: function() {
    this.on('change:name', function() {
      this.set('path', '/static/main/' + this.get('name'));
      this.set('blur', '/static/blur/' + this.get('name'));
      this.set('img_width', (window.innerWidth - 200) + 'px');
      this.set('img_height', window.innerHeight + 'px');
    });
  }
});

  var ImageView = Backbone.View.extend({
    initialize: function() {
      this.model.on('change:name', this.render, this);
    },
    
    template: _.template($('#image-template').html()),

    render: function() {
      console.log("Start ImageView.render()");
      this.$el.html(this.template(this.model.toJSON()));

      return this;
    }
  });

var BackgroundImageView = Backbone.View.extend({
  el: '#main',
  
  template: _.template($('#background-template').html()),

  initialize: function() {
    this.model.on('change:name', this.render, this);
  },
  
  render: function() {
    this.$el.html(this.template(this.model.toJSON()));

    return this;
  }
});

var mainImage = new MainImage();

var ThumbView = Backbone.View.extend({
  template: _.template($('#thumb-template').html()),

  events: {
    'click .thumb': 'onClick'
  },

  render: function() {
    this.$el.html(this.template(this.model.toJSON()));

    return this;
  },

  onClick: function() {
    // console.log("Thumb's click");
    // console.log("id = " + this.model.get('id'));
    mainImage.set({'id': this.model.get('id'),
                   'name': this.model.get('name'),
                   'create_date': this.model.get('create_date')});
  }
});

  var ImageCollection = Backbone.Collection.extend({
    model: Image,
    url: "/photos",

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
        throw new Error("Collection fetch error");
    }
  });

  var ImageCollectionView = Backbone.View.extend({
    el: '#app',
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
      this.collection.bind("reset", this.render);
      // this.collection.fetch();
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

// var backgroundView = new BackgroundImageView({ model: mainImage});
var mainImageView = new ImageView({ model: mainImage});
var imageCollection = new ImageCollection;
imageCollection.fetch({
  success: function() {
    var imageCollectionView = new ImageCollectionView({
      collection: imageCollection
    });
    // $('#main').append(backgroundView.render().el);
    //backgroundView.render();
    

    
    //$('#background').append("<div>imageCollectionView.render().el</div>");

    //$('#app').append(imageCollectionView.render().el);
    imageCollectionView.render();
    var img = imageCollection.at(0);

    if (img != null) {
      mainImage.set({'id': img.get('id'), 'name': img.get('name'),
                    'create_date': img.get('create_date')});
    }
  }
});

$('#main').append(mainImageView.render().el);

var groupCollection = new GroupCollection;
groupCollection.fetch({
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
