from ATvis import paramSingleFig_Work, paramSingleFig_Presentation, paramSingleFig_MNRAS, paramSingleFig_MNRAS


__all__ = [ 'paramSingleFig_SED_Work',
            'paramSingleFig_SED_Presentation',
            'paramSingleFig_SED_MNRAS',
            'paramSingleFig_SED_SmallPresentation',
            'paramSingleFig_FMCI_XP_Presentation',
            'paramSingleFig_FMCI_XP_Work'
            ]

# # -----------------------------------------------
# # Geometry values: good for work
# # -----------------------------------------------
# paramSingleFig_Work = dict(figsize_points     = [720,480],
#                            axes_boxes         = [[0.12,.1375,.86,.8]],
#                            ylabel_left_x      = 0.01,
#                            ylabel_left_y      = None, # ylabel at axes center
#                            xlabel_bottom_y    = 0.01,
#                            xlabel_bottom_x    = None, # xlabel at axes center
#                            label_fontsize     = 20,
#                            ticklabel_fontsize = 11)

# # -----------------------------------------------
# # Geometry values: good for presentations
# # -----------------------------------------------
# paramSingleFig_Presentation = dict(label_fontsize     = 22,
#                                    ticklabel_fontsize = 14)

# # -----------------------------------------------
# # Geometry values: good for single column MNRAS figure
# # -----------------------------------------------
# paramSingleFig_MNRAS = dict( figsize_inch       = [3.5,2.254],
#                              axes_boxes         = [[0.129,.155,.857,.823]],
#                              label_fontsize     = 11,
#                              ticklabel_fontsize = 9   )


# -----------------------------------------------
# SED plots: Geometry values: 
# -----------------------------------------------
paramSingleFig_SED_Work                                    = dict( axes_boxes = [[0.18,.1375,.79,.8]] )
# Presentation
paramSingleFig_SED_Presentation                            = paramSingleFig_Presentation.copy()
paramSingleFig_SED_Presentation['axes_boxes']              = [[0.18,.1375,.79,.8]]
paramSingleFig_SED_Presentation['ticklabel_fontsize']      = 17
# MNRAS
paramSingleFig_SED_MNRAS                                   = paramSingleFig_MNRAS.copy()
paramSingleFig_SED_MNRAS['axes_boxes']                     = [[0.19,.1375,.78,.8]]
# MNRAS
paramSingleFig_SED_SmallPresentation                       = paramSingleFig_MNRAS.copy()
paramSingleFig_SED_SmallPresentation['axes_boxes']         = [[0.22,.18,.76,.79]]
paramSingleFig_SED_SmallPresentation['ticklabel_fontsize'] = 11
paramSingleFig_SED_SmallPresentation['label_fontsize']     = 12


# -----------------------------------------------
# FMCI XP plots: Geometry values: 
# -----------------------------------------------
paramSingleFig_FMCI_XP_Work = paramSingleFig_Work.copy()
paramSingleFig_FMCI_XP_Work['figsize_points'] = [840,480]                
paramSingleFig_FMCI_XP_Work['axes_boxes']     = [[0.1025,.1375,.922,.8]] 
paramSingleFig_FMCI_XP_Work['xlabel_bottom_x']= 0.47                     

paramSingleFig_FMCI_XP_Presentation = paramSingleFig_Presentation.copy()
paramSingleFig_FMCI_XP_Presentation['figsize_points'] = [840,480]
paramSingleFig_FMCI_XP_Presentation['axes_boxes']     = [[0.1025,.1375,.922,.8]]
paramSingleFig_FMCI_XP_Presentation['xlabel_bottom_x']= 0.47                    
