__all__ = [ 'paramMPP_MNRAS',
            'paramMPP_Timeseries_MNRAS' ]

paramMPP_MNRAS = dict( fig_width_abs       = 7,
                       aspect_ratio        = 1.618,
                       dx_pad_abs          = 0.1,
                       dy_pad_abs          = 0.1,
                       left_margin_abs     = 0.45,
                       right_margin_abs    = 0.05,
                       top_margin_abs      = 0.2,
                       bottom_margin_abs   = 0.35,
                       xlabel_bottom_y_abs = 0.01,
                       xlabel_top_y_abs    = 0.01,
                       ylabel_left_x_abs   = 0.01,
                       ylabel_right_x_abs  = 0.10,
                       label_fontsize      = 11,
                       ticklabel_fontsize  = 9,
                       yticklabel_fontsize = 8,
                       timelabel_format    = '%.3f',
                       timelabel_fontsize  = 9
                       )

paramMPP_Timeseries_MNRAS = paramMPP_MNRAS.copy()
paramMPP_Timeseries_MNRAS['top_margin_abs'] = 0.1
