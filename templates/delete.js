 $( document ).ready(function() {

document.getElementById('tags-input').addEventListener('keypress', function(event) {
        if (event.keyCode == 13) {
            event.preventDefault();
            if ($("#tags-input").serialize()){
               $('.btn').click();
            }
        }
    });

$('.btn').click(function() {
  tagSerialized = $("#tags-input").serialize();
  tagName = cleanFormValue(tagSerialized);
  addTag(tagName);
})

  function addTag(tagName){
  tagLink = $('<a>',
    {
      href: '#' /*+ tag +'/'+imageName*/
    });

    innerSpan = $('<span>',{
      class: "",
      text: tagName,
    });
	innerSpan.appendTo(tagLink);
    tagLink.appendTo($(".tags"));
  }
  });

function cleanFormValue(tagSerialized){
  tagArray = tagSerialized.split("=");
  tagArray.shift();
  tagName = tagArray.toString();
  decodedTag = decodeURIComponent(tagName);
  return decodedTag;
}