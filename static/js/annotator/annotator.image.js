Annotator.Plugin.Image = function (element) {
  if ($('img', element).length === 0)
    return;
  return {
    pluginInit: function() {
      if (!Annotator.supported())
        return;
      anno_bridge.push({el: element, an: this.annotator});
      var xannotator = this.annotator;
      console.log(xannotator, element);
      this.annotator.subscribe("annotationUpdated", function(annotation) {
        console.log("annotationUpdated", annotation);
      });
      anno.addHandler('onAnnotationCreated', function(annotation) {
        var xanno = Object.assign({}, annotation);
        xannotator.publish('annotationCreated', xanno);
        console.log("Create: ", annotation);
      });
      anno.addHandler('onAnnotationUpdated', function(annotation) {
        xannotator.publish('annotationUpdated', Object.assign({}, annotation));
        console.log("Update: ", annotation);
      });
      anno.addHandler('onAnnotationRemoved', function(annotation) {
        xannotator.publish('annotationDeleted', Object.assign({}, annotation));
        console.log("Remove: ", annotation);
      });
      this.annotator.subscribe("annotationsLoaded", function(annotations) {
        for(let annoitem of annotations) {
          if ('shapes' in annoitem) {
            var xanno = Object.assign({}, annoitem);
            console.log("Load: ", xanno);
            anno.addAnnotation(xanno);
          }
        }
      });
    },
  }
}
