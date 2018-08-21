function addSubmit(ev) {
      ev.preventDefault();
      // var request = new XMLHttpRequest();
      
      var request = new XMLHttpRequest();

      request.addEventListener('load', addShow);
      request.open('POST', url);
      request.send(formd);
      // request.send(sti);
      console.log('submitted');
    // request.open('POST', {{ url_for('add')|tojson }});
    // request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
    // request.send(formd);
    }
    function addShow() {
      var data = JSON.parse(this.responseText);
      // var span = document.getElementById('result');
      // span.innerText = data.result;
      console.log(data);
    }
    function consolee() {
      console.log("clicked");
    }
    
    var form = document.getElementById('calc');
    var sti = "stringtest";
    var formd = new FormData();
      formd.append('first', "tests");
      formd.append('first', "testa");
      formd.append('first', "testb");
      formd.append('first', "testc");
      formd.set('first', "testz");
      formd.append('last', "asfasf");
    form.addEventListener('submit', addSubmit);