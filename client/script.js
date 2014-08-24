var Sidebar = Backbone.Model.extend({
  promptColor: function() {
    var cssColor = prompt("Пожалуйста, введите CSS-цвет:");
    this.set({color: cssColor});
  }
});

window.sidebar = new Sidebar;

sidebar.on('change:color', function(model, color) {
  $('#sidebar').css({background: color});
});

sidebar.set({color: 'red'});

sidebar.promptColor();