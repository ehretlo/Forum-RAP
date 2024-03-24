const Button = document.querySelector("#btn");

if (Button){
    Button.addEventListener("click",() => {
    Button.classList.toggle("btn-secondary");
    Button.classList.toggle("btn-primary");
    
    Button.textContent = Button.classList.contains("btn-primary") ? "<3" : "Like here";
    })

}
else{
    console.error("Could not find button");
}
