Annotator.Plugin.Image = function (element, types) {
  if ($('img', element).length === 0)
    return;
  return {
    traceMouse: false,
    pluginInit: function() {
      if (!Annotator.supported())
        return;
      let annotator = this.annotator;
      var startPoint = null;
      var activeRect = null;
      var imgWidth = $('img', element).width();
      var imgHeight = $('img', element).height();
      var type_count = 0;
      var highlights = [];
      
      for (let xi in types)
        type_count++;
      
      function modifyHighlightColor(annotation) {
        let highlight = highlights['d'+annotation.id];
        if (highlight && type_count > 0) {
          $(highlight.div).css('border-color', types['t'+annotation.atype].color);
        }
      }
      
      function createHighlight(left, top, width, height, annotation) {
        var div = document.createElement('div');
        $(div).addClass('annotator-hl annotator-img-rect').css({
          left: left+'px', 
          top: top+'px', 
          width: width+'px',
          height: height+'px',
        });
        $('.annotator-wrapper', element).append(div);
        if (annotation) {
          $(div).data('annotation', annotation)
            .data('annotation-id', annotation.id);
          div.rect = {left: left, top: top, right: left+width, bottom: top+height};
          highlights['d'+annotation.id] = {'div': div, 'annotation': annotation};
          modifyHighlightColor(annotation);
          $(div).off('mouseover');
          $(div).on('mouseover', function(event) {
            var pos = $(event.target).position();
            var x = pos.left + event.offsetX;
            var y = pos.top + event.offsetY;
            var annotations = [];
            for (let i in highlights) {
              let highlight = highlights[i];
              let rect = highlight.div.rect;
              if (x > rect.left && x < rect.right && y > rect.top && y < rect.bottom)
                annotations.push(highlight.annotation);
            }
            if (annotations.length > 1) {
              window.setTimeout(function() {
                annotator.showViewer(annotations, {left: x, top: y});
              }, 100);
            }
          });
        }
        return div;
      }
      
      $('img', element).mousedown(function(e) {
        if (!annotator.options.readOnly && e.which === 1) {
          annotator.editor.hide();
          self.traceMouse = true;
          startPoint = {x: e.offsetX, y: e.offsetY};
          activeRect = createHighlight(e.offsetX, e.offsetY, 0, 0, null);
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
        if (self.traceMouse) {
          $(activeRect).css({left: Math.min(e.offsetX, startPoint.x), top: Math.min(e.offsetY, startPoint.y), width: Math.abs(e.offsetX - startPoint.x)+'px', height: Math.abs(e.offsetY - startPoint.y)+'px'});
        }
        return false;
      });

      this.annotator.subscribe("annotationsLoaded", function(annotations) {
        for(let i in annotations) {
          let item = annotations[i];
          var rect = item.shapes[0].geometry;
          createHighlight(rect.x * imgWidth, rect.y * imgHeight, rect.width * imgWidth, rect.height * imgHeight, item);
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
        var rect = annotation.shapes[0].geometry;
        (function verify_id() {
          if (!annotation.id) {
            window.setTimeout(verify_id, 5);
          } else {
            createHighlight(rect.x * imgWidth, rect.y * imgHeight, rect.width * imgWidth, rect.height * imgHeight, annotation);
          }
        })();
      });
      
      this.annotator.subscribe("annotationUpdated", function(annotation) {
        modifyHighlightColor(annotation);
      });
      
      this.annotator.subscribe("annotationEditorHidden", function(editor) {
        if (activeRect) {
          $(activeRect).remove();
          activeRect = null;
        }
      });
      
      this.annotator.subscribe("annotationDeleted", function(annotation) {
        let highlight = highlights['d'+annotation.id];
        if (highlight) {
          $(highlight.div).remove();
          delete highlights['d'+annotation.id];
        }
      });
    },
  }
}
