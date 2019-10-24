let dropdown = document.getElementById('selDataYear');
dropdown.length = 0;

let defaultOption = document.createElement('option');
defaultOption.text = 'Year';

dropdown.add(defaultOption);
dropdown.selectedIndex = 0;

const url = '/census_income_to_rent_dataset/years';



fetch(url)  
  .then(  
    function(response) {  
      if (response.status !== 200) {  
        console.warn('Looks like there was a problem. Status Code: ' + 
          response.status);  
        return;  
      }

      // Examine the text in the response  
      response.json().then(function(data) {  
        let option;
    
    	for (let i = 0; i < data.length; i++) {
          option = document.createElement('option');
      	  option.text = data[i];
      	  option.value = data[i];
      	  dropdown.add(option);
    	}    
      });  
    }  
  )  
  .catch(function(err) {  
    console.error('Fetch Error -', err);  
  });



