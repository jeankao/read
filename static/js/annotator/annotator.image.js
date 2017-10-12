Annotator.Plugin.Image = function (element, types) {
  if ($('img', element).length === 0)
    return;

  return {
    traceMouse: false,
    annotations: [],
    pluginInit: function() {
      if (!Annotator.supported())
        return;
      let annotator = this.annotator;
      var startPoint = null;
      var activeRect = null;
      var imgWidth = $('img', element).width();
      var imgHeight = $('img', element).height();
      let _annotations = this.annotations = [];

      function modifyRectColor(annotation) {
        for (let i in _annotations) {
          let item = _annotations[i];
          if (item.annotation.id === annotation.id && types.length > 0) {
            $(item.div).css('border-color', types['t'+item.annotation.atype].color);
          }
        }        
      }
      
      function createRectDiv(left, top, width, height) {
        var div = document.createElement('div');
        $(div).addClass('annotator-img-rect').css({
          left: left+'px', 
          top: top+'px', 
          width: width+'px',
          height: height+'px',
          pointerEvents: 'none',
        });
        $('.annotator-wrapper', element).append(div);
        return div;
      }
      
      $('img', element).mousedown(function(e) {
        if (!annotator.options.readOnly && e.which === 1) {
          annotator.editor.hide();
          self.traceMouse = true;
          startPoint = {x: e.offsetX, y: e.offsetY};
          activeRect = createRectDiv(e.offsetX, e.offsetY, 0, 0);
        }
        return false;
      });

      $('img', element).mouseup(function(e) {
        self.traceMouse = false;        
        startPoint = null;
        if (!annotator.options.readOnly) {
          annotator.viewer.hide();
          annotator.showEditor({text: ''}, {left: e.offsetX, top: e.offsetY});
        }
        return false;
      });
      
      $('img', element).mousemove(function(e) {
        if (!self.traceMouse) {
          if (!annotator.viewer.isShown()) {
            var left = e.offsetX / imgWidth, 
                top = e.offsetY / imgHeight;
            var annotations = [];
            var rect = {};
            for (let i in _annotations) {
              let item = _annotations[i];
              rect = item.annotation.shapes[0].geometry;
              if (left >= rect.x && left <= rect.x+rect.width && top >= rect.y && top <= rect.y + rect.height) {
                annotations.push(item.annotation);
              }
            }
            if (annotations.length > 0) {
              annotator.showViewer(annotations, {left: e.offsetX, top: e.offsetY});
              annotator.editor.hide();
            }
          }
        } else {
          $(activeRect).css({left: Math.min(e.offsetX, startPoint.x), top: Math.min(e.offsetY, startPoint.y), width: Math.abs(e.offsetX - startPoint.x)+'px', height: Math.abs(e.offsetY - startPoint.y)+'px'});
        }
        return false;
      });

      this.annotator.subscribe("annotationsLoaded", function(annotations) {
        for(let i in annotations) {
          let item = annotations[i];
          var rect = item.shapes[0].geometry;
          var rectDiv = createRectDiv(rect.x * imgWidth, rect.y * imgHeight, rect.width * imgWidth, rect.height * imgHeight);
          if (types.length > 0)
            $(rectDiv).css('border-color', types['t'+item.atype].color);
          _annotations.push({annotation: item, div: rectDiv});
        }
      });

      this.annotator.subscribe('annotationEditorSubmit', function(editor, annotation) {
        var aid = annotation.id || 0;
        if (!aid) {
          var rect = {
            left: parseInt($(activeRect).css('left').slice(0,-2)),
            top: parseInt($(activeRect).css('top').slice(0, -2)), 
            width: $(activeRect).width(),
            height: $(activeRect).height(),
          };
          annotation.shapes = [{
            geometry: {
              y: rect.top / imgHeight, 
              x: rect.left / imgWidth, 
              width: rect.width / imgWidth,
              height: rect.height / imgHeight,
            },
            style: {},
          }];          
          annotator.publish('annotationCreated', annotation);
        } else
          annotator.publish('annotationUpdated', annotation);
      });
      
      this.annotator.subscribe('annotationCreated', function(annotation) {
        console.log('annotationCreate', annotation);
        var rect = annotation.shapes[0].geometry;
        var rectDiv = createRectDiv(rect.x * imgWidth, rect.y * imgHeight, rect.width * imgWidth, rect.height * imgHeight);
        _annotations.push({annotation: annotation, div: rectDiv});
        modifyRectColor(annotation);
      });
      
      this.annotator.subscribe("annotationUpdated", modifyRectColor);
      
      this.annotator.subscribe("annotationEditorHidden", function(editor) {
        if (activeRect) {
          $(activeRect).remove();
          activeRect = null;
        }
      });
      
      this.annotator.subscribe("annotationDeleted", function(annotation) {
        for (let i in _annotations) {
          if (_annotations[i].annotation.id === annotation.id) {
            $(_annotations[i].div).remove();
            _annotations.splice(i, 1);
            break;
          }
        }
      });
      
      this.annotator.subscribe("annotationEditorShown", function(editor, annotation) {
        if (annotation.shapes) {
          //var rect = annotation.shapes[0].geometry;
          //$(editor.element).css({left: rect.x * imgWidth, top: (rect.y + rect.height) * imgHeight});
          //$('html, body').scrollTop($(editor.element).offset().top);
        }
      });
    },
  }
}
