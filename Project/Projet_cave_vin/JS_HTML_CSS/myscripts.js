			function dosetItem() {
				var parcelle = document.getElementById("parc").value;
                var cepage =  document.getElementById("cepage").value;
                var re = RegExp('^[0-9]*$');
                if (re.test(parcelle) && parcelle!=="" && cepage!==""){    //obliger de tester que le cepage soit vide car lors d'une saisie le menue déroulant est une value="" si aucun cépage de saisie.
                     for (i=0; i<=localStorage.length-1;i++){
                         if (localStorage.key(i)===parcelle){
                            e = localStorage.getItem(localStorage.key(i));
                            r = e.split(","); //concatener avec une , 
                            console.log(r) //r0 à r(n) longeur 
                            for (j=0; j<=r.length-1;j++){
                                if(r[j]==cepage){
                                    alert("La clé existe déja");
                                    document.getElementById("parc").value="";
                                    document.getElementById("cepage").value="";
                                    afficher();
                                    return;
                                }
                            }
                            e = e+","+cepage;
                            localStorage.setItem(parcelle,e);
                            document.getElementById("parc").value="";
                            document.getElementById("cepage").value="";
                            afficher();
                            return;}
                            }
                    localStorage.setItem(parcelle,cepage);
                    document.getElementById("parc").value="";
                    document.getElementById("cepage").value="";
                    afficher();
                    }
                else {
                    document.getElementById("parc").value="";
                    document.getElementById("cepage").value="";
                    alert("Saisie Incorrecte :\nVérifiez que tous les champs soient remplis.\nVerifiez que votre \"Parcelle\" ne comporte que des chiffres");
                }
                
   		        } 
			
				<!-- fonction d'affichage liste -->
			function afficher() {
				 var key = "";
				 var paires = "<tr class=\"first\"><td><b>Parcelle</b></td><td><b>Cépage</b></td></tr>\n";
				 var i=0;
				 for (i=0; i<=localStorage.length-1; i++) {
					key = localStorage.key(i);
				 paires+="<tr><td>"+key+"</td>\n<td>"+localStorage.getItem(key)+"</td></tr>\n";
				 }
				 if (paires == "<tr class=\"first\"><td><b>Parcelle</b></td><td><b>Cépage</b></td></tr>\n"){
					paires += "<tr><td><i>Vide</i></td>\n<td><i>Vide</i></td></tr>\n";}
				 document.getElementById('paires').innerHTML = paires;
				 }
				 
				 
				 <!-- fontion pour modifier -->
			function dogetItem(){
                var parcelle = document.getElementById("parc").value;
                var cepage =  document.getElementById("cepage").value;
                var re = RegExp('^[0-9]*$')
                if (re.test(parcelle) && parcelle!=="" && cepage!==""){
                    for (i=0; i<=localStorage.length-1;i++){
                        if (localStorage.key(i)===parcelle){
                            localStorage.setItem(parcelle,cepage);
                            document.getElementById("parc").value="";
                            document.getElementById("cepage").value="";
                            afficher();
                            return;
                        }                   
                    }
                    document.getElementById("parc").value="";
                    document.getElementById("cepage").value="";
                    alert("La clé n'existe pas et ne peut donc être modifiée\nUtilisez la fonction \"Ajouter\" si vous souhaitez ajouter cette clé");
                }

                else{
                    document.getElementById("parc").value="";
                    document.getElementById("cepage").value="";
                    alert("Saisie Incorrecte :\nVérifiez que tous les champs soient remplis.\nVerifiez que votre \"Parcelle\" ne comporte que des chiffres");
                }
            }
			
				  <!-- fonction pour modifier -->
			function doremoveItem(){
                var parcelle = document.getElementById("parc").value;
                var cepage =  document.getElementById("cepage").value;
                if (localStorage.getItem(parcelle)==cepage){
                    localStorage.removeItem(parcelle);
                    document.getElementById("parc").value="";
                    document.getElementById("cepage").value="";
                    afficher();
                    return;
                }

                else if (localStorage.getItem(parcelle).includes(cepage)){
                    r = localStorage.getItem(parcelle).split(",");
                    for (i=0;i<=r.length-1;i++){
                        if(r[i]==cepage){
                            r.splice(i,1);                            
                       }
                    }
                    console.log(r);
                    localStorage.setItem(parcelle,r);
                }
                else {
                    alert("Il n'existe pas de cépage associé à cette parcelle")
                }

                document.getElementById("parc").value="";
                document.getElementById("cepage").value="";
                afficher();
                }
				
				function listeCepage() {
                var selection = document.getElementById("cepage2").value;
                var listeParcelle = [];
                var design ="<th>"+document.getElementById("cepage2").value+"</th>\n";
                for (i=0;i<=localStorage.length-1;i++){
                    key = localStorage.key(i);
                    if ( localStorage.getItem(key).includes(selection)) {

                        design += "<tr><td>"+key+"</td></tr>\n";
                        listeParcelle.push(key)
                        }}
                if (design=="<th>"+document.getElementById("cepage2").value+"</th>\n"){
                    design+="<tr><td><i>Vide</i></td></tr>\n";
					alert("C'est vide !!")
					
                }
                console.log(listeParcelle) 
                document.getElementById('listing').innerHTML = design;                               
            }
			
				 <!-- fonction pour supprimer la liste -->
			// function doClear() {
				 // localStorage.clear();
				 // afficher();
				  // }