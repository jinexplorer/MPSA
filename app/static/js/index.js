function load_sucess()
{
    alert("hello");
}
var curIndex = 0;
var loadinged=0
function loading(time)
{
    if(loadinged==0)
    {
        setInterval("changeImg()", time);
        loadinged=1;
    }
}
function changeImg(){
	var arr = new Array();
	arr[0] = "../static/image/1.png";
	arr[1] = "../static/image/2.png";
	arr[2] = "../static/image/3.png";
	arr[3] = "../static/image/4.png";
	arr[4] = "../static/image/5.png";
	arr[5] = "../static/image/6.png";
	var obj = document.getElementById("obj");
	if(curIndex == arr.length - 1)
	    curIndex=0;
	else
	    curIndex=curIndex+1;
	obj.src = arr[curIndex];
}
