# json.dump()
 converts your Python dictionary (data) into JSON format and writes it to the file f.    
# ecnoding="utf-8"
ensures Unicode characters (like Urdu or emojis) are saved correctly.
# indent=4
Without it, all data will be in one long line.
# ensure_ascii=False
 → allows non-ASCII characters (like Urdu or emojis) to be saved properly without escaping.








# 1️⃣ Check if the request is POST

# if request.method == "POST":
Django differentiates between GET (just loading the page) and POST (form submitted).
This line ensures that the code inside runs only when the admin submits the form.

# if old_question:
 → only runs when editing an existing FAQ

# pop() 
 → removes the old question-answer pair so it can be replaced safely
# None
 is just a default value to avoid an error if the key does not exist.
# knowledge[question] = answer
Now the dictionary adds the new answer under the same question key.



# {% csrf_token %}
 → Django requires this for security. It prevents others from sending fake requests to your site.





