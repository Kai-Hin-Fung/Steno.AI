import time
from rev_ai import apiclient

def transcribe_audio (file_path):
    # String containing your access token
    access_token = "02djDGwoi7m4mxzz-ntDQ5TfZbuqIpC947Jy6BIcvLkcpoONP2pdVXE6_VMmLq7SJrYfNDZlnmy-elqtrFhvgP0aYGM-0"
    # Create your api client
    client = apiclient.RevAiAPIClient(access_token)

    job = client.submit_job_local_file(file_path)

    print("Submitted Job")

    while True:

        # Obtains details of a job in json format
        job_details = client.get_job_details(job.id)
        status = job_details.status.name

        print("Job Status : {}".format(status))

        # Checks if the job has been transcribed
        if status == "IN_PROGRESS":
            time.sleep(5)
            continue

        elif status == "FAILED":
            print("Job Failed : {}".format(job_details.failure_detail))
            break

        if status == "TRANSCRIBED":
            # Getting a list of current jobs connected with your account
            # The optional parameters limits the length of the list.
            # starting_after is a job id which causes the removal of
            # all jobs from the list which were created before that job
            list_of_jobs = client.get_list_of_jobs(limit=None, starting_after=None)

            # obtain transcript text as a string for the job.
            transcript_text = client.get_transcript_text(job.id)
            print(transcript_text)

            # obtain transcript text as a json object for the job.
            transcript_json = client.get_transcript_json(job.id)

            # obtain transcript object for the job.
            transcript_obj = client.get_transcript_object(job.id)

            # obtain captions for the job.
            captions = client.get_captions(job.id)

            break

    # Use the objects however you please

    # Once you are done with the job, you can delete it.
    # NOTE : This will PERMANENTLY DELETE all data related to a job. Exercise only
    # if you're sure you want to delete the job.
    # client.delete_job(job.id)
    print("Job Submission and Collection Finished.")
    return transcript_text
