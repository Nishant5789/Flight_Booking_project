
const convert_text_to_time = (time)=>
{
    hour = Math.floor(time).toString().padStart(2, '0');
    min = ((time - hour)*60).toFixed(0).padStart(2, '0');
    result = hour+":"+min+":00"
    console.log(result);
}
convert_text_to_time('23')
