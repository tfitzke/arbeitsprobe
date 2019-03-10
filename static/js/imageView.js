
/* Fügt visuell ein Tag hinzu. Die tatsächliche Eintragung in die sqlite-DB passiert in der ajax zuvor (siehe imageView.html) */
function addTag(tag, data_container){
    var tagName = tag;
    if (!data_container.imageTags.includes(tagName) ){
        tagLink = $('<a>',
            {
                href: '#'
        });
        innerSpan = $('<span>',{
            class: "tag label label-info margin2",
            text: tagName,
            click: function(){
                deleteTag($(this));
            } 
        });
        data_container.imageTags.push(tagName);
        innerSpan.appendTo(tagLink);
        tagLink.appendTo($(".tags"));
    }
}

/* lädt alle Tags, die in der sqlite-DB sind, auf die Seite*/
function init_tags(data_container){
    if (data_container.imageTags.length != 0){
        for (i=0; i<data_container.imageTags.length; i++){
            tagLink = $('<a>',
                {
                    href: '#'
                });
            innerSpan = $('<span>',{
                class: "tag label label-info margin2",
                text: data_container.imageTags[i],
                click: function(){
                    deleteTag($(this));
                }
            });
            innerSpan.appendTo(tagLink);
            tagLink.appendTo($(".tags"));
        }
    }
}
/* löscht tag per ajax und von der website*/
function deleteTag(thisTag){
    tagName =thisTag.text();
    console.log(tagName);
    var url = window.location.pathname;   
    url_array = url.split("/");
    photoPath = url_array[url_array.length-1];
    var data = {
      "tagName":  tagName,
      "photoName": photoPath
          };
    if (data  && data.tagName.length > 0){
        $.ajax({
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(data),
                dataType: 'json',
                url: '/deleteTag',
                success: function (e) {
                    console.log(e);
                    window.location('/deleteTag');
                },
                error: function(error) {
                    console.log(error);
                }
        });
        thisTag.remove();
    } else {
        console.log("Tag undefined");
    }
}
/* serialized und decoded URI */
function cleanFormValue(serializedForm){
  tagArray = tagSerialized.split("=");
  tagArray.shift();
  tagName = tagArray.toString();
  decodedTag = decodeURIComponent(tagName);
  return decodedTag;
}