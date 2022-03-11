import { Component, OnInit } from '@angular/core';
import { WebService } from '../web.service';
import { ActivatedRoute } from '@angular/router';
import { FormBuilder, Validators } from '@angular/forms';
import { AuthService } from '@auth0/auth0-angular';

@Component({
  selector: 'episodeReviews',
  templateUrl: './episode_reviews.component.html',
  styleUrls: ['./episode_reviews.component.css']
})
export class EpisodeReviewsComponent  {

  updatedReview;
  episodes_list: any = [];
  reviews: any=[];
  newReview

  constructor(public webService: WebService,
    private route: ActivatedRoute,
    public formBuilder: FormBuilder,
    public authService: AuthService){}

    
  ngOnInit(){
    this.webService.getReviews(this.route.snapshot.params.id)

    this.updatedReview = this.formBuilder.group({
      rating: ["", Validators.required],
      review: ["", Validators.required]
    });

  }  

  DeleteReview(review){
      this.webService.deleteReview(review._id);
      this.webService.getReviews(this.route.snapshot.params.id);
      window.location.reload
  }

  updatedSubmit(review_id) {
    this.webService.updateReview(this.updatedReview.value, review_id)
    this.webService.getReviews(this.route.snapshot.params.id);
    window.location.reload
    // this.webService.getReviews(this.route.snapshot.params.id)
  }

}
