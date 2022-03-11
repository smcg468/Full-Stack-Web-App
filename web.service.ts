import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Injectable } from '@angular/core';
import { stringify } from "querystring";
import { Subject } from 'rxjs'

@Injectable()
export class WebService {

    constructor(private http: HttpClient){

    }

    o_episodes_list;
    officeEpisodesSubject = new Subject();
    episodes_list: any = this.officeEpisodesSubject.asObservable()

    //episodes_list: any;


    

    getOfficeEpisodes(page:number){

        return this.http.get('http://localhost:5000/v1.0/office_episodes?pn=' + page)
            .subscribe((response: any) => {
                this.o_episodes_list = response
                this.officeEpisodesSubject.next(this.o_episodes_list);
            });

    }

/*
    getOfficeEpisodes(page: number){
        return this.http.get(`http://localhost:5000/v1.0/office_episodes?pn=` + page);
    }
*/

    o_episode_list;
    officeEpisodeSubject = new Subject();
    episode_list: any = this.officeEpisodeSubject.asObservable();
    officeEpisodeId: any;


    getOfficeEpisode(id){
        this.http.get(`http://localhost:5000/v1.0/office_episodes/` + id)
          .subscribe((response:any) => {
              this.o_episode_list = response
              this.officeEpisodeSubject.next (this.o_episode_list);
              this.officeEpisodeId = id
            });
    }

    o_season_list;
    officeSeasonSubject = new Subject();
    season_list: any = this.officeSeasonSubject.asObservable();

    getOfficeSeason(season:number){
        return this.http.get('http://localhost:5000/v1.0/office_episodes/season/?s=' + season)
            .subscribe((response: any) => {
                this.o_season_list = response
                this.officeSeasonSubject.next(this.o_season_list);
            });

    }

/*
    getOfficeEpisode(id: any){
        return this.http.get(`http://localhost:5000/v1.0/office_episodes/`+ id);
    }
*/
    review_list;
    episodeReview = new Subject();
    episodeReview_list: any = this.episodeReview.asObservable()

    getReviews(reviews_id: any) {
        return this.http.get(`http://localhost:5000/v1.0/episode_reviews/` + reviews_id)
            .subscribe((response:any)  => {
                this.review_list = response
                this.episodeReview.next(this.review_list);
            })


    }


    newReview(review: any){
        let postData = new FormData();
        postData.append("username", review.username);
        postData.append("rating", review.rating);
        postData.append("review", review.review);
    

        this.http.post(`http://localhost:5000/v1.0/episode_reviews/${this.officeEpisodeId}/`, postData)
            .subscribe((response:any) => {
                    this.getReviews(this.officeEpisodeId)
                }
            )

    }

    updateReview(review, review_id) {
        let postData = new FormData();
        postData.append("rating", review.rating);
        postData.append("review", review.review);

        this.http.put(`http://localhost:5000/v1.0/episode_reviews/${review_id}/`, postData)
            .subscribe((response:any) => {
                    console.log("Review updated successfully");
                }
            )
    }


    deleteReview(review_id) {
        this.http.delete(`http://localhost:5000/v1.0/episode_reviews/${review_id}/`)
            .subscribe((response:any) => {
                    console.log("Review deleted successfully");
                }
            )
    }

}


