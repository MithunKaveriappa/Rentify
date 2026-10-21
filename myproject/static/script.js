// ---- Navbar scroll shadow ----
window.addEventListener("scroll", function() {
    const nav = document.querySelector("nav");
    if(window.scrollY > 18)
        nav.style.boxShadow = "0 6px 18px rgba(0,188,212,0.18)";
    else
        nav.style.boxShadow = "0 4px 8px rgba(0,0,0,0.2)";
});

// ---- Smooth scroll for all local links ----
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        let target = document.querySelector(this.getAttribute('href'));
        if(target)
            target.scrollIntoView({ behavior: 'smooth', block: 'center'});
    });
});

// ---- Button ripple effect ----
document.querySelectorAll('button').forEach(function(btn) {
    btn.addEventListener('click', function(e){
        let ripple = document.createElement("span");
        ripple.className = "ripple";
        ripple.style.left = e.offsetX+"px";
        ripple.style.top  = e.offsetY+"px";
        btn.appendChild(ripple);
        setTimeout(()=>{ ripple.remove(); }, 500);
    });
});

// ---- Animate messages when shown ----
window.onload = function() {
    setTimeout(function(){
        var msg = document.getElementById('message');
        if (msg) msg.style.display='none';
    }, 3200);
};

// ---- Footer year auto-update ----
let year = new Date().getFullYear();
let yearEls = document.querySelectorAll('.footer-bottom-year');
yearEls.forEach(function(el){
    el.textContent = year;
});

// ---- Table highlight on hover ----
document.querySelectorAll('table tr').forEach(function(row){
    row.addEventListener('mouseover',function(){ row.style.backgroundColor="#e0effc"; });
    row.addEventListener('mouseout',function(){ row.style.backgroundColor=""; });
});

// ---- Pulse unread notifications ----
document.querySelectorAll('.unread-notification').forEach(function(el){
    el.style.boxShadow = '0 0 16px #00bcd4';
    setTimeout(function() { el.style.boxShadow = ''; }, 1400);
});

// ---- Ripple CSS for buttons ----
const style = document.createElement('style');
style.innerHTML = `
.ripple {
    position: absolute;
    width: 35px;
    height: 35px;
    background: rgba(0,188,212,0.3);
    border-radius: 50%;
    pointer-events: none;
    transform: scale(0);
    animation: ripple-effect .39s linear;
    z-index: 12;
}
@keyframes ripple-effect {
    to { transform: scale(2.2); opacity: 0; }
}`;
document.head.appendChild(style);
