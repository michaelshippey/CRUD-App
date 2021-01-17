var title; 
var posterURL;
var plot;

function searchMovie(){ 

            var api_key = "c61db953"
            var movie = $("#input").val()
            var url = "https://www.omdbapi.com/?apikey="+api_key+"&"

        $.ajax({
            
            method:'GET',
            url:url+"&t="+movie,
            success:function(data){
                console.log(data)
                title = data.Title
                posterURL = data.Poster
                
                 var newWin = window.open("review.html?movieName="+title+"&URL="+posterURL)
                

                 newWin.onload = function(){
                     newWin.document.getElementById("title").innerHTML = title
                     newWin.document.getElementById("poster").src = posterURL    
                   };
                   
               
            }           
     });
      
    }
