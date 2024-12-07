from django.db import connection
from django.shortcuts import render, redirect, get_object_or_404
from .models import Application, User_Person, ApplicationMatch
#jobskill
from .forms import ApplicationForm, UserForm
from django.http import JsonResponse


#return to home page 
def home(request):
    return render(request, 'home.html')

#application list - get all the application objects 
#render the application_list html page - pass in the applications as input
def application_list(request):
    applications = Application.objects.all()
    return render(request, 'application_list.html', {'applications': applications})


#add an application 
#render the application_list html page - pass in the filled form as input
def add_application(request):
    if request.method == 'POST': 
        #send the post request as input to forms 
        form = ApplicationForm(request.POST)
        #if form is valid set it to the default user 
        #if form is valid set it to the default user 
        if form.is_valid():
            application = form.save(commit=False)
            user_person, _ = User_Person.objects.get_or_create(
                email='mahab@example.com', 
                defaults={
                    'name': 'maha', 
                }
            )
            application.user = user_person
            application.save()
            #go back to the applications refreshed page 
            return redirect('application_list')
        else:
            print("Form errors:", form.errors)
        form = ApplicationForm()
    applications = Application.objects.all()
    return render(request, 'application_list.html', {'form': form, 'applications': applications})


#delete the selected checkbox applications 
def delete_application(request):
    if request.method == 'POST':
        #get the select ids 
        selected_ids = request.POST.getlist('applications')
        #add them to the list of valid ids 
        valid_ids = [int(app_id) for app_id in selected_ids if app_id.strip().isdigit()]
        if valid_ids:
            Application.objects.filter(app_id__in=valid_ids).delete()       
        return redirect('application_list')
    return redirect('application_list')

    


#edit the application selected using the edit radio button next to each application 
def edit_application(request, app_id):
    #get the application with the app_id of the selected application 
    application = get_object_or_404(Application, pk=app_id)

    if request.method == 'POST':
        #send the post request as input to forms 
        form = ApplicationForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            return redirect('application_list')
    else:
        form = ApplicationForm(instance=application)
    
    #go back to the edit applications html page using the form input of the current application information 
    return render(request, 'edit_application.html', {'form': form})

#helper method to get the percentage of how your skills match to the job skills 
def calculate_and_save_match_percentage(input_skills):
    #clean and filter the skills list 
    input_skills_list = [skill.strip() for skill in input_skills.split(",")]

    #Traverse through the applications and get the skills of each application
    applications = Application.objects.all()  
    for application in applications:
        #application skills 
        app_skills = application.get_skills()
        #your skills 
        input_skills_set = set(input_skills_list)  
        app_skills_set = set(app_skills)  
        #get the union of the skills 
        matched_skills = input_skills_set.intersection(app_skills_set) 
        #Get the match percent using the number of matched skills by the total input skills 
        match_percentage = ((len(matched_skills)/len(input_skills_set))*100) if input_skills_set else 0

        #add the new object to the model - app-match which has the app_id and the match percent 
        match_record, created = ApplicationMatch.objects.get_or_create(application=application, defaults={'match_percentage': match_percentage})

        #if the object has not been created then assign the match percent value
        if not created:
            match_record.match_percentage = match_percentage
            match_record.save()

#Application analysis home page 
def application_analysis(request):
    return render(request, 'application_analysis.html')

#Prepared Statement 2 - Count Applications 
#method to count the number of applications 
def count_applications(request):
    #get the start and end date 
    if request.method == 'GET':
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        
        #error code: if the start and end date are not entered 
        if not start_date or not end_date:
            return JsonResponse({'error': 'Start date and end date are required!'}, status=400)

        #print(start_date)
        #print(end_date)
        # Prepared statement to get the number of rows that have a date between the start and end date 
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) 
                FROM tracker_application 
                WHERE date_applied BETWEEN %s AND %s
            """, [start_date, end_date])
            count = cursor.fetchone()[0]
            #print(count)

        #return count 
        return JsonResponse({'application_count': count})


#Prepared statements 1 - match percent
def generate_report(request):
    if request.method == 'GET':
        skills_input = request.GET.get('skills', '')
        if skills_input:
            #filter and clean the strings input 
            skills = skills_input 
            #calc match percents 
            calculate_and_save_match_percentage(skills)  

            #SQL Query Prepared Statement to get all the app ids with a match percentage > 80
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT am.application_id, am.match_percentage
                    FROM tracker_applicationmatch am
                    WHERE am.match_percentage > %s
                    ORDER BY am.match_percentage DESC
                """, [80])
                results = cursor.fetchall()

            #Get the application object of the application with a high match percent 
            applications_with_high_match = []
            for row in results:
                application_id, match_percentage = row
                application = Application.objects.get(app_id=application_id)
                applications_with_high_match.append({
                    'application_id': application.app_id,
                    'company': application.company,
                    'position': application.position,
                    'match_percentage': match_percentage
                })

            return JsonResponse({'applications': applications_with_high_match})

    return render(request, 'application_analysis.html')

#Prepared statements 3 - Generate report 2 about the number of application in each status pool
def generate_report_two(request):
    if request.method == 'GET':
        #get the number/count of application in status stage 
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    SUM(CASE WHEN status = 'Interviewing' THEN 1 ELSE 0 END) AS interviewed_count,
                    SUM(CASE WHEN status = 'Offer Received' THEN 1 ELSE 0 END) AS offer_received_count,
                    SUM(CASE WHEN status = 'Rejected' THEN 1 ELSE 0 END) AS rejected_count,
                    COUNT(*) AS total_count
                FROM tracker_application
            """)
            result = cursor.fetchone()

        #print("Query Result:", result)  

        if result:
            interviewed_count, offer_received_count, rejected_count, total_count = result
        else:
            interviewed_count = offer_received_count = rejected_count = total_count = 0

        status_counts = {
            'interviewed_count': interviewed_count,
            'offer_received_count': offer_received_count,
            'rejected_count': rejected_count,
            'total_count': total_count
        }
        #return the output to the html page 
        #print("Returning JSON Response:", status_counts)  
        return JsonResponse(status_counts)

    #default to main subpage 
    return render(request, 'application_analysis.html')