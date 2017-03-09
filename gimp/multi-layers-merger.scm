;;Autor: Markus Rietz 
;;www.3d-animandesign.de

(script-fu-register 
 "multi-layers-merger"
 "Multi Layers Merger"
 "Merges layers between images"
 "Markus Rietz"
 "Markus Rietz, GNU"
 "04/04/2012"
 ""
 
 SF-IMAGE    "select prime image" 1;Image_AImage
 SF-DRAWABLE "select layer" 1;DrawableA_Layer
 SF-TOGGLE "Active element marks the foreground of the result " TRUE;Toggle_AsForeground
 SF-TOGGLE "Use only active Layer" TRUE;Toggle_UseActiveLayerOnly
 SF-IMAGE  "Second Image to merge with: " 2;Image_SImage
 SF-TOGGLE "Merge layers on the same levels only " TRUE;Toggle_SameLevels
 SF-TOGGLE "Append Unmerged Layers" TRUE;Toggle_OutputUnmerged
 )

(script-fu-menu-register "multi-layers-merger"
                         "<Image>/Layer/")

(define	(multi-layers-merger 	Image_AImage
                                DrawableA_Layer
                                Toggle_AsForeground
                                Toggle_UseActiveLayerOnly
                                Image_SImage
                                Toggle_SameLevels
                                Toggle_OutputUnmerged )
  ;___________________________________Additional Variables
  (let*(
        (NewImageWidth  (car(gimp-drawable-width DrawableA_Layer )  ) )
        (NewImageHeight (car(gimp-drawable-height DrawableA_Layer )  ) )  
         
        (Image_Buffer   (car(gimp-image-new NewImageWidth NewImageHeight RGB)  ) )
        (IntA 0)
        (IntB 0)
        (OuterLoopTimes 1)
        (InnerLoopTimes 1)
        (ExtraLoopTimesA 0)
        (ExtraLoopTimesB 0)
        (LoopInnerLoop 1)
        (ORG_LList  (vector->list(cadr (gimp-image-get-layers Image_AImage ) )))
        (SEC_LList  (vector->list(cadr (gimp-image-get-layers Image_SImage ) )))
        )
 ;____________________________________DEF Part I
 
 
  (define (image-merge-layer-to-image Image_Input
                                      Drawable_LoopUpperLayer
                                      Drawable_LoopLowerLayer
                                      )  
    (let*(
          (LowerLayerCopy 0)
          (UpperLayerCopy 0)
          (NewLayer 0)
          )
    
      (if (not (= Drawable_LoopLowerLayer -1)) 
          (begin
            (set! LowerLayerCopy (car (gimp-layer-new-from-drawable Drawable_LoopLowerLayer Image_Input )))
            (gimp-image-insert-layer Image_Input LowerLayerCopy 0 -1 )
            ))
      
      (if (not (= Drawable_LoopUpperLayer -1))
          (begin
            (set! UpperLayerCopy (car (gimp-layer-new-from-drawable Drawable_LoopUpperLayer Image_Input )))
            (gimp-image-insert-layer Image_Input UpperLayerCopy 0 -1 )
            ))
      (if   (and (not(= Drawable_LoopLowerLayer -1)) (not(= Drawable_LoopUpperLayer -1)))
            (begin(set! NewLayer (car (gimp-image-merge-down Image_Input UpperLayerCopy EXPAND-AS-NECESSARY )))) 
            )
      Image_Input
      )
    )

      

    ;______________________________________DEF Part II_______________________________
    
    (define (get-LayerID-by-counter image 
                                    counter
                                    )
                               ;returns LayerID
                               ;on image error return FALSE
      (let*((List '())
            (LayerID -1)
            
            ) 
        (set! List (vector->list(cadr (gimp-image-get-layers image ) )))
        (while (> counter 0)
               (if (not (= (length List) 0))
                   (begin
                     (set! LayerID  (car List))
                     (set! List  (cdr List))
                     
                     )
                   (begin
                     (set! LayerID -1)
                     )
                   )
               (set! counter (- counter 1))
               )
        LayerID     
        ))
    
    ;____________________________________DEF PART III
    (define (layerID-get-image-layer-ID activeimage 
                                        activelayer
                                        targetimage
                                        )
      
      (let*(
            (testvarA 0)
            (testvarB 0)
            (Output -1)
            )
        
         (set! testvarA (car(gimp-image-get-item-position  activeimage activelayer)))
         (set! testvarB (car(gimp-image-get-layers Image_AImage )))
        
      (if (not (> (car(gimp-image-get-item-position  activeimage activelayer)) (car(gimp-image-get-layers Image_AImage )) )) 
          (begin
            (if (not (= activelayer -1)) ;test for invalid items for gimp-image-get-item-position 
                (begin
                  (set! Output (get-LayerID-by-counter targetimage (+ (car(gimp-image-get-item-position  activeimage activelayer)) 1)))
                  )
                ))
          )
        Output
        ))
   
    ;_____________________________________ Main Description Part
 (set! IntA (car(gimp-image-get-layers Image_AImage ) ))
    (set! IntB (car(gimp-image-get-layers Image_SImage ) ))
    
    (gimp-image-undo-freeze Image_Buffer )

         
    (set! OuterLoopTimes IntA)
    (set! InnerLoopTimes IntB)

    
     (if (= Toggle_OutputUnmerged TRUE)
         (begin
           (set! ExtraLoopTimesA IntA)
           (set! ExtraLoopTimesB IntB)
         ))
    
    (if (and (= Toggle_UseActiveLayerOnly FALSE) (= Toggle_SameLevels TRUE) ) 
        (begin
          (if  (< IntA IntB) 
               (begin
                 (if (= Toggle_OutputUnmerged TRUE)
                     (begin
                        (set! OuterLoopTimes IntB)
                        (set! InnerLoopTimes IntB)
                        ) 
                     (begin
                       (set! OuterLoopTimes IntA)
                       (set! InnerLoopTimes IntA)
                       )))
                 (begin
                   (if (= Toggle_OutputUnmerged TRUE)
                       (begin
                         (set! OuterLoopTimes IntA)
                         (set! InnerLoopTimes IntA)
                         ) 
                       (begin
                         (set! OuterLoopTimes IntB)
                         (set! InnerLoopTimes IntB)
                         ))
                   ))
          ))
          
      
          (if (= Toggle_UseActiveLayerOnly TRUE)
              (begin
                (set! OuterLoopTimes 1)
                (if (= Toggle_SameLevels TRUE)
                    (begin 
                      (set! InnerLoopTimes  1)
                      
                      ))
                )
              )
 ;___________________________________Append_First_LIFO________________________First Part for First and Second Image ______________
        
  (if (not (and (= Toggle_UseActiveLayerOnly FALSE) (= Toggle_SameLevels TRUE) ))        
        ;_________append unmerged    
(begin
    (if (= Toggle_UseActiveLayerOnly TRUE)
        (begin 
          (while (> ExtraLoopTimesA 0)
                 (if (not (= DrawableA_Layer (get-LayerID-by-counter Image_AImage ExtraLoopTimesA)))
                     (begin
                       (set! Image_Buffer (image-merge-layer-to-image Image_Buffer (get-LayerID-by-counter Image_AImage ExtraLoopTimesA) -1))
                       ))
          (set! ExtraLoopTimesA (- ExtraLoopTimesA 1))
          )))
       
       
    ;____________________________Append_First_LIFO________________________Scond Part for Second Image only ______________________
    ;RESET
   
    (if (= Toggle_SameLevels TRUE)     
        (begin
          (while (> ExtraLoopTimesB 0)
                
                 (if (not (= DrawableA_Layer (layerID-get-image-layer-ID Image_SImage (get-LayerID-by-counter Image_SImage ExtraLoopTimesB)  Image_AImage)))
                     (begin
                     
                       (set! Image_Buffer (image-merge-layer-to-image Image_Buffer (get-LayerID-by-counter Image_SImage ExtraLoopTimesB) -1))
                       ))
          (set! ExtraLoopTimesB (- ExtraLoopTimesB 1))
          )))
    ;_____________________________________________________________________________________________________________________________   
))
        

 
    (while (> OuterLoopTimes 0)
           
           ;VERY IMPORTANT AND FOR SAME LEVEL MERGE EFFECTS INNER LOOP ONLY################   
           (set! LoopInnerLoop  InnerLoopTimes)
           (if (= Toggle_SameLevels TRUE)
               (begin 
                 (set! LoopInnerLoop  1)
                 ))
           ;###############################################################################
    
          (while (> LoopInnerLoop 0)
                 
         
                 (if (= Toggle_UseActiveLayerOnly TRUE)
                     (begin 
                       (if (= Toggle_SameLevels TRUE)
                            (begin 
                              (if(= Toggle_AsForeground TRUE)
                                 (begin 
                                   (set! Image_Buffer (image-merge-layer-to-image Image_Buffer DrawableA_Layer (layerID-get-image-layer-ID Image_AImage DrawableA_Layer Image_SImage) ))
                                   )
                                 (begin 
                                   (set! Image_Buffer (image-merge-layer-to-image Image_Buffer (layerID-get-image-layer-ID Image_AImage DrawableA_Layer Image_SImage) DrawableA_Layer))
                                   ))
                              )
                            (begin
                              
                              (if(= Toggle_AsForeground TRUE)
                                 (begin 
                                   (set! Image_Buffer (image-merge-layer-to-image Image_Buffer DrawableA_Layer (get-LayerID-by-counter Image_SImage LoopInnerLoop)))
                                   )
                                 (begin 
                                   (set! Image_Buffer (image-merge-layer-to-image Image_Buffer (get-LayerID-by-counter Image_SImage LoopInnerLoop) DrawableA_Layer)) 
                                   ))
                              )
                            )
                       )
                     (begin 
                        (if (= Toggle_SameLevels TRUE)
                            (begin 
                              (if(= Toggle_AsForeground TRUE)
                                 (begin 
                                   (set! Image_Buffer (image-merge-layer-to-image Image_Buffer (get-LayerID-by-counter Image_AImage OuterLoopTimes) (get-LayerID-by-counter Image_SImage OuterLoopTimes) ))
                                   )
                                 (begin 
                                   (set! Image_Buffer (image-merge-layer-to-image Image_Buffer (get-LayerID-by-counter Image_SImage OuterLoopTimes) (get-LayerID-by-counter Image_AImage OuterLoopTimes))) 
                                   ))
                              )
                            (begin
                              (if(= Toggle_AsForeground TRUE)
                                 (begin 
                                   (set! Image_Buffer (image-merge-layer-to-image Image_Buffer (get-LayerID-by-counter Image_AImage OuterLoopTimes) (get-LayerID-by-counter Image_SImage LoopInnerLoop)))
                                   )
                                 (begin 
                                   (set! Image_Buffer (image-merge-layer-to-image Image_Buffer (get-LayerID-by-counter Image_SImage LoopInnerLoop) (get-LayerID-by-counter Image_AImage OuterLoopTimes))) 
                                   ))
                              
                              ))
                        ))
                   
                 ;############################### END Handle Images 
                 (set! LoopInnerLoop (- LoopInnerLoop 1))
                 )
          
          (set! OuterLoopTimes (- OuterLoopTimes 1))
          )
    ;FINAL OUTPUT
       
      (gimp-image-undo-thaw Image_Buffer )
 (gimp-display-new Image_Buffer)
    )
 )
    